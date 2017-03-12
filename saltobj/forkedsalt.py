# coding: utf-8

import os, copy, json, signal, logging
import salt.minion
import salt.utils
from salt.version import __version__ as saltversion

from saltobj.config import SaltConfigMixin

RS = '\x1e' # default suffix of \x1e is ascii for record
            # separator RS

class MasterMinionJidNexter(object):
    def get_jids(self): return []
    def get_jid(self):  pass
    def get_load(self): pass

    def __init__(self, opts):
        # this is meant to somewhat replicate what happens in
        # salt/runners/jobs.py in print_job()

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
        for jid in sorted(self.get_jids()):
            # This is a continuation of the things that happen in
            # salt/runners/jobs.py in print_job()

            # It is trickey, the master doesn't really store the event in the
            # job cache it has to be reconstructed from various sources and
            # some extra trash has to be removed to make it sorta look right
            # again see note/ping-return-vs-ping-jobcache.js

            # This is meant to be completely different form what happens in
            # salt/runners/jobs.py in _format_jid_instance(jid,job), but
            # has borrowed ideas …

            load = self.get_load(jid)
            mini = load.pop('Minions', ['local'])

            try:
                jdat = self.get_jid(jid)
            except Exception as e:
                jdat = {'_jcache_exception': "exception trying to invoke get_jid({0}): {1}".format(jid,e)}

            for id in mini:
                mjdat = jdat.get(id)
                fake_return = {
                    "jid": jid,
                    "id": id,
                    "fun": load.get('fun'),
                    "fun_args": load.get('arg'),
                    "cmd": "_return", 
                    "_stamp": salt.utils.jid.jid_to_time(jid), # spurious!! this isn't really the return time

                    # I can't think of any way to fake these in a general way
                    # and the jobcache doesn't store them
                    "retcode": None,
                    "success": None,
                }

                fake_return.update(mjdat)

                tag = "uevent/job_cache/{0}/ret/{1}".format(jid,id)
                _jdat = {'get_load':load, 'get_jid_{0}'.format(id): mjdat}

                yield {'tag': tag, '_raw':_jdat, 'data': fake_return}

    def next(self):
        if self.g:
            try:
                return self.g.next()
            except StopIteration:
                self.g = False

class ForkedSaltPipeWriter(SaltConfigMixin):
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
        self.log = logging.getLogger('ForkedSaltPipeWriter')

        self.get_event_args = { 'full': True }
        if saltversion.startswith('2016'):
            self.get_event_args['auto_reconnect'] = True

        if self.replay_file:
            print "opening replay_file={0}".format(self.replay_file)
            self.replay_fh = open(self.replay_file,'r')
        else:
            self.replay_fh = None

        if self.replay_job_cache:
            self.mmjn = MasterMinionJidNexter(self.mmin_opts)

        if self.replay_only:
            self.sevent = None
        else:
            # NOTE: salt-run state.event pretty=True
            #       is really salt.runners.state.event()
            # which is really salt.modules.state.event()
            # which is really salt.utils.event.get_event()
            self.sevent = salt.utils.event.get_event(
                    'master', # node= master events or minion events
                    self.salt_opts['sock_dir'],
                    self.salt_opts['transport'],
                    opts=self.salt_opts,
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
                exit(0)
                raise Exception("dead")

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
