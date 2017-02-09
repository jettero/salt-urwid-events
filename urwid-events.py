#!/usr/bin/env python2

import signal, os, copy, json
import urwid
import salt.config, salt.utils

def setup_logging(file='urwid-events.log', format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
    import logging, sys
    fh = logging.FileHandler(file)
    fh.setFormatter(logging.Formatter(format))
    log = logging.getLogger('urwid')
    log.addHandler(fh)
    log.setLevel(logging.DEBUG)
    log.debug("logging configured")
    class LogWriter(object):
        def __init__(self,fn):
            self.fn = fn
        def write(self,message):
            self.fn( message.rstrip() )
        def flush(self):
            pass
    sys.stderr = LogWriter(log.warning)
    return log
log = setup_logging()
event_no = 0

class mysevent(object):
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

    def pipe_loop(self, write_fd):
        log.debug("entering pipe_loop")

        if self.ppid is not None or self.kpid is not None:
            log.debug("already looping??")
            return

        self.ppid = os.getpid()
        self.kpid = os.fork()

        log.debug("ppid={0} kpid={1}".format(self.ppid,self.kpid))

        if self.kpid:
            log.debug("ppid={0} kpid={1} I am parent and I'm returning".format(self.ppid,self.kpid))
            return

        def see_ya(*x):
            log.debug("ppid={0} kpid={1} I am kid, see_ya()".format(self.ppid,self.kpid))
            exit(0)
        signal.signal(signal.SIGINT, see_ya)

        log.debug("ppid={0} kpid={1} I am kid and I'm looping".format(self.ppid,self.kpid))
        while True:
            e = self.next()
            if e is None:
                log.debug('null event, re-looping')
                continue
            j = json.dumps(e, indent=2)
            log.debug("got event: {0}".format(j))
            os.write( write_fd, j )

    def see_ya(self):
        if self.kpid:
            os.kill(self.kpid, signal.SIGINT)

class EventApplication(object):
    pallet = [
        ('banner', 'black', 'light gray'),
        ('streak', 'black', 'dark red'),
        ('bg',     'black', 'dark blue'),
    ]
    event_no = 0

    def __init__(self):
        def exit_on_q(input):
            if input in ('q', 'Q'):
                raise urwid.ExitMainLoop()

        self.status = urwid.Text(('banner', u"wating for events"))

        map1 = urwid.AttrMap(self.status, 'streak')
        fill = urwid.Filler(map1, 'top')
        map2 = urwid.AttrMap(fill, 'bg')

        self.loop = urwid.MainLoop(map2, self.pallet, unhandled_input=exit_on_q)
        self.write_fd = self.loop.watch_pipe(self.got_event)
        self.sevent = mysevent()
        self.sevent.pipe_loop(self.write_fd)

    def run(self):
        self.loop.run()

    def see_ya(self,*x):
        log.debug("os.getpid={0} sevent.kpid={1} I am global, see_ya()".format(os.getpid(),self.sevent.kpid))
        self.sevent.see_ya()
        raise urwid.ExitMainLoop()

    def status(self,status):
        self.status.set_text(('banner', status))

    def got_event(self,data):
        self.event_no += 1
        if self.event_no == 1: self.status(u'got event')
        else: self.status(u'got {0} events'.format(event_no))

def main():
    app = EventApplication()
    signal.signal(signal.SIGINT, app.see_ya)
    app.run()

if __name__=="__main__":
    main()
    print "\n\n\n"
