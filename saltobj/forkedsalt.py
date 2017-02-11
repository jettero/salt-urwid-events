
import os, copy, json
import salt.config, salt.utils
import logging

log = logging.getLogger('ForkedSaltPipeWriter')

__all__ = ['ForkedSaltPipeWriter']

class ForkedSaltPipeWriter(object):
    ppid = kpid = None

    def __init__(self):
        # look at /usr/lib/python2.7/site-packages/salt/modules/state.py in event()
        self.master_config = salt.config.master_config('/etc/salt/master')
        self.minion_config = salt.config.minion_config('/etc/salt/minion')

        self.config = copy.deepcopy(self.minion_config)
        self.config.update( copy.deepcopy(self.master_config) )

        self.sevent = salt.utils.event.get_event(
                'master', # node= master events or minion events
                self.config['sock_dir'],
                self.config['transport'],
                opts=self.config,
                listen=True)

    def next(self):
        return self.sevent.get_event(full=True, auto_reconnect=True)

    def main_loop(self, callback):
        while True:
            e = self.next()
            if e is None:
                log.debug('null event, re-looping')
                continue
            j = json.dumps(e, indent=2)
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