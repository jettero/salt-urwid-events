#!/usr/bin/env python2

import os, copy, json
import urwid
import salt.config, salt.utils

class mysevent(object):
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
        self.ppid = os.getpid()
        self.kpid = os.fork()

        if self.kpid:
            return

        while True:
            e = self.next()
            if e is None:
                continue
            os.write( write_fd, json.dumps(e, indent=2) )

def main():
    def exit_on_q(input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    txt = urwid.Text(u"Hello World")
    fill = urwid.Filler(txt, 'top')
    loop = urwid.MainLoop(fill)

    def got_event(data):
        txt.set_text( 'pipe data:\n{0}'.format(data) )

    write_fd = loop.watch_pipe(got_event)

    sevent = mysevent()
    sevent.pipe_loop(write_fd)

    loop.run()

if __name__=="__main__":
    main()
