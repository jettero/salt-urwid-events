# coding: utf-8

import os, copy, json, signal, logging
import salt.config, salt.minion, salt.config
from salt.version import __version__ as saltversion

RS = '\x1e' # default suffix of \x1e is ascii for record
            # separator RS

class MasterMinionJidNexter(object):
    def get_jids(self): return []
    def get_jid(self):  pass
    def get_load(self): pass

    def __init__(self, opts):
        self.log = logging.getLogger('MasterMinionJidNexter')
        mminion = salt.minion.MasterMinion(opts)
        for fn in ('get_jids', 'get_jid', 'get_load',):
            for i in ('ext_job_cache', 'master_job_cache',):
                fn_full = '{0}.{1}'.format( opts.get(i), fn )
                if fn_full in mminion.returners:
                    self.log.debug("using MasterMinion.returners[{0}] for MasterMinionJidNexter.{1}".format(fn_full,fn))
                    setattr(self, fn, mminion.returners[fn_full])
                    break
        self.g = self.gen()

    def gen(self):
        for i in self.get_jids():
            # this is trickey, the master doesn't really store the event in the
            # job cache it has to be reconstructed from various sources and
            # some extra trash has to be removed to make it sorta look right
            # again

            load = self.get_load(i)
            mini = load.pop('Minions')

            jid = load.get('jid', '<>')
            for id in mini:
                job = { 'tag': 'salt/job/{0}/ret/{1}'.format(jid,id), 'data': load }
                yield job

    def next(self):
        if self.g:
            try:
                return self.g.next()
            except StopIteration:
                self.g = False

class ForkedSaltPipeWriter(object):
    ppid = kpid = None
    evno = 0

    def __init__(self, args=None, preproc=None, replay_file=None, replay_only=False, replay_job_cache=None):
        self.preproc          = preproc
        self.replay_file      = replay_file
        self.replay_only      = replay_only
        self.replay_job_cache = replay_job_cache

        # overwrite all self vars from args (where they match)
        if args:
            for k,v in vars(args).iteritems():
                if hasattr(self,k):
                    setattr(self,k,v)

        if not isinstance(self.preproc,list):
            if isinstance(self.preproc,tuple):
                self.preproc = list(self.preproc)
            elif self.preproc is not None:
                self.preproc = [self.preproc]
            else:
                self.preproc = []

        self._init2()

    def _init2(self):
        # look at /usr/lib/python2.7/site-packages/salt/modules/state.py in event()
        self.master_config = salt.config.master_config('/etc/salt/master')
        self.minion_config = salt.config.minion_config('/etc/salt/minion')

        self.log = logging.getLogger('ForkedSaltPipeWriter')

        self.get_event_args = { 'full': True }
        if saltversion.startswith('2016'):
            self.get_event_args['auto_reconnect'] = True

        self.config = copy.deepcopy(self.minion_config)
        self.config.update( copy.deepcopy(self.master_config) )

        if self.replay_file:
            print "opening replay_file={0}".format(self.replay_file)
            self.replay_fh = open(self.replay_file,'r')
        else:
            self.replay_fh = None

        if self.replay_job_cache:
            self.mmjn = MasterMinionJidNexter(self.config)

        if self.replay_only:
            self.sevent = None
        else:
            # NOTE: salt-run state.event pretty=True
            #       is really salt.runners.state.event()
            # which is really salt.modules.state.event()
            # which is really salt.utils.event.get_event()
            self.sevent = salt.utils.event.get_event(
                    'master', # node= master events or minion events
                    self.config['sock_dir'],
                    self.config['transport'],
                    opts=self.config,
                    listen=True)

    def add_preproc(self, *preproc):
        for p in preproc:
            if isinstance(p,list) or isinstance(p,tuple):
                self.add_preproc(*p)
            elif p is not None and p not in self.preproc:
                self.preproc.append(p)

    def next(self):
        ev = None

        if self.replay_fh:
            ev_text = ''
            while True:
                line = self.replay_fh.readline()
                if line:
                    if line.strip(): ev_text += line
                    else: break
                else:
                    self.replay_fh = self.replay_fh.close()
                    break
            if ev_text:
                # this is a pretty weak pre-parse/sanity-check, but it works
                if ev_text.lstrip().startswith('{') and ev_text.rstrip().endswith('}'):
                    ev = json.loads(ev_text)
                    ev['_from_replay'] = self.replay_file

        elif self.replay_job_cache:
            ev = self.mmjn.next()
            if ev is None:
                self.replay_job_cache = self.mmjn = False

        elif self.sevent:
            ev = self.sevent.get_event( **self.get_event_args )

        else:
            self.log.info("replay only and replay is finished, exit normally")
            exit(0)

        for pprc in self.preproc:
            if ev is not None:
                ev = pprc(ev)

        if ev is not None:
            ev['_evno'] = self.evno
            self.evno += 1
            return json.dumps(ev, indent=2)

    def main_loop(self, callback):
        while True:
            if not os.path.isfile('/proc/{0.ppid}/cmdline'.format(self)):
                self.log.debug("our ppid={0.ppid} seems to be missing. breaking mainloop now".format(self))
                return

            j = self.next()
            if j is None:
                self.log.debug('null event, re-looping')
                continue

            self.log.debug("main_loop callback with {0} byte(s)".format(len(j)))
            callback(j)

    def _write_to_pipe(self, data, prefix='json:', suffix=RS):
        if prefix:
            self.log.debug('writing prefix={0}'.format(repr(prefix)))
            os.write( self.write_fd, prefix )

        self.log.debug("write_to_pipe with {0} byte(s)".format(len(data)))
        os.write( self.write_fd, data )

        if suffix:
            self.log.debug('writing suffix={0}'.format(repr(suffix)))
            os.write( self.write_fd, suffix )

    def pipe_loop(self, write_fd):
        self.log.debug("entering pipe_loop")

        if self.ppid is not None or self.kpid is not None:
            self.log.debug("already looping??")
            return

        self.ppid = os.getpid()
        self.kpid = os.fork()

        if self.kpid:
            return

        def see_ya(*x):
            exit(0)

        signal.signal(signal.SIGINT, see_ya)

        self.write_fd = write_fd
        self.main_loop(self._write_to_pipe)

    def see_ya(self):
        if self.kpid:
            os.kill(self.kpid, signal.SIGINT)
