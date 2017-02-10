#!/usr/bin/env python2

import signal, os, copy, json
import urwid
from forkedsalt import ForkedSaltPipeWriter

def setup_logging(file='urwid-events.log', format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
    import logging, sys
    fh = logging.FileHandler(file)
    fh.setFormatter(logging.Formatter(format))
    logging.root.addHandler(fh)
    logging.root.setLevel(logging.DEBUG)
    logging.root.debug("logging configured")
    log = logging.getLogger('urwid')
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

class EventApplication(object):
    pallet = [
        ('status', 'yellow', 'dark blue'),
    ]
    event_no = 0

    def __init__(self):
        self.status_txt = urwid.Text(('status', u"wating for events"))

        self.jids = [urwid.Text('wtf')]
        self.jids_listwalker = urwid.SimpleListWalker(self.jids)
        self.jids_listbox = urwid.ListBox(self.jids_listwalker)
        self.main_frame = urwid.Frame(self.jids_listbox, footer=urwid.AttrMap(self.status_txt, 'status'))

        args   = (self.main_frame,self.pallet,)
        kwargs = { 'unhandled_input': self.exit_on_q }
        try:
            log.info("trying to use curses")
            kwargs['screen'] = urwid.curses_display.Screen()
            self.loop = urwid.MainLoop(*args, **kwargs)
        except Exception as e:
            log.debug("self.loop exception: {0}".format(e))
            log.info("failed to use curses, trying the default instead")
            if 'screen' in kwargs:
                del kwargs['screen']
            self.loop = urwid.MainLoop(*args, **kwargs)

        self._write_fd = self.loop.watch_pipe(self.got_event)
        self.sevent = ForkedSaltPipeWriter()
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

    def handle_salt_data(self, data):
        log.debug('trying to handle salt data')
        if 'data' in data:
            log.debug('return data found')
            if 'tag' in data:
                log.info('salt event tag: {0}'.format(data['tag']))
            job_data = data['data']
            if 'jid' in job_data:
                log.debug('trying to append jid={0} to the listbox'.format(job_data['jid']))
                self.jids_listwalker.append(urwid.Text(job_data['jid']))

    def got_event(self,data):
        if data.lower().strip() == 'q':
            self.see_ya('q')

        self.event_no += 1
        if self.event_no == 1: self.status(u'got event')
        else: self.status(u'got {0} events'.format(self.event_no))

        if data.startswith('json:'):
            try:
                self.handle_salt_data(json.loads(data[5:]))
            except Exception as e:
                log.warning("exception trying to handle json data: {0}".format(e))
                pass

def main():
    app = EventApplication()
    def sig(signal,frame):
        app.hear_event('q')
    signal.signal(signal.SIGINT, app.see_ya)
    app.run()
    print "\nevents collected: {0}".format( app.event_no )

if __name__=="__main__":
    main()
