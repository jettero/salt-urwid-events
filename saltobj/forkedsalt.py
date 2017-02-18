
import os, copy, json
import logging
import salt.config, salt.utils
from salt.version import __version__ as saltversion

log = logging.getLogger('ForkedSaltPipeWriter')

class ForkedSaltPipeWriter(object):
    ppid = kpid = None

    def __init__(self, preproc=None, replay_file=None, replay_only=False):
        # look at /usr/lib/python2.7/site-packages/salt/modules/state.py in event()
        self.master_config = salt.config.master_config('/etc/salt/master')
        self.minion_config = salt.config.minion_config('/etc/salt/minion')

        self.get_event_args = { 'full': True }
        if saltversion.startswith('2016'):
            self.get_event_args['auto_reconnect'] = True

        self.replay_file = replay_file
        self.replay_only = replay_only

        self.preproc = []
        self.add_preproc(preproc)

        self.config = copy.deepcopy(self.minion_config)
        self.config.update( copy.deepcopy(self.master_config) )

        if replay_file:
            self.replay_fh = open(replay_file,'r')
        else:
            self.replay_fh = None

        if replay_only:
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
                ev = json.loads(ev_text)
                ev['_from_replay'] = self.replay_file

        if not ev:
            if self.sevent:
                ev = self.sevent.get_event( **self.get_event_args )
            else:
                log.info("replay only and replay is finished, exit normally")
                exit(0)

        if ev is not None:
            for pprc in self.preproc:
                ev = pprc(ev)

        if ev is not None:
            return json.dumps(ev, indent=2)

    def main_loop(self, callback):
        while True:
            j = self.next()
            if j is None:
                log.debug('null event, re-looping')
                continue
            log.debug("got event: {0}".format(j))
            callback(j)

    def pipe_loop(self, write_fd):
        log.debug("entering pipe_loop")

        if self.ppid is not None or self.kpid is not None:
            log.debug("already looping??")
            return

        self.ppid = os.getpid()
        self.kpid = os.fork()

        if self.kpid:
            return

        def see_ya(*x):
            exit(0)

        signal.signal(signal.SIGINT, see_ya)
        self.main_loop(lambda j: os.write( write_fd, 'json:'+j ))

    def see_ya(self):
        if self.kpid:
            os.kill(self.kpid, signal.SIGINT)
