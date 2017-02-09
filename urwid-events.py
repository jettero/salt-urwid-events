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

        if self.kpid:
            return

        def see_ya(*x):
            exit(0)
        signal.signal(signal.SIGINT, see_ya)

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
        self.status_txt = urwid.Text(('banner', u"wating for events"))

        map1 = urwid.AttrMap(self.status_txt, 'streak')
        fill = urwid.Filler(map1, 'top')
        map2 = urwid.AttrMap(fill, 'bg')

        self.loop = urwid.MainLoop(map2, self.pallet, unhandled_input=self.exit_on_q)
        self._write_fd = self.loop.watch_pipe(self.got_event)
        self.sevent = mysevent()
        self.sevent.pipe_loop(self._write_fd)

    def exit_on_q(self,input):
        if input in ('q', 'Q'):
            self.see_ya('q')

    def run(self):
        self.loop.run()
        self.sevent.see_ya()

    def see_ya(self,*x):
        if len(x):
            log.debug("received signal={0}".format(x[0]))
        self.sevent.see_ya()
        raise urwid.ExitMainLoop()

    def status(self,status):
        self.status_txt.set_text(('banner', status))

    def hear_event(self, x):
        os.write( self._write_fd, x )

    def got_event(self,data):
        if data.lower().strip() == 'q':
            self.see_ya('q')

        self.event_no += 1
        if self.event_no == 1: self.status(u'got event')
        else: self.status(u'got {0} events'.format(self.event_no))

        if data.startswith('json:'):
            data = json.loads(data[5:])
            # XXX: do something with this data nao

def main():
    app = EventApplication()
    def sig(signal,frame):
        app.hear_event('q')
    signal.signal(signal.SIGINT, app.see_ya)
    app.run()
    print "\nevents collected: {0}".format( app.event_no )

if __name__=="__main__":
    main()
