# coding: utf-8

import signal, os, json
import urwid

import misc
import saltobj
import wrapper

class EventApplication(object):
    pallet = [
        ('status', 'yellow', 'dark blue'),
    ]
    event_no = 0

    def __init__(self, args):
        self.args = args

        self._pdat= ''

        self.status_txt = urwid.Text(('status', u"wating for events"))
        self.log = misc.setup_file_logger('urwidobj.EventApplication')

        self.events = []
        self.events_listwalker = urwid.SimpleListWalker(self.events)
        self.events_listbox = urwid.ListBox(self.events_listwalker)
        self.main_frame = urwid.Frame(self.events_listbox, footer=urwid.AttrMap(self.status_txt, 'status'))

        _a   = (self.main_frame,self.pallet,)
        _kw = { 'unhandled_input': self.exit_on_q }
        try:
            self.log.info("trying to use curses")
            _kw['screen'] = urwid.curses_display.Screen()
            self.loop = urwid.MainLoop(*_a, **_kw)
        except Exception as e:
            self.log.debug("self.loop exception: {0}".format(e))
            self.log.info("failed to use curses, trying the default instead")
            if 'screen' in _kw:
                del _kw['screen']
            self.loop = urwid.MainLoop(*_a, **_kw)

        self._write_fd = self.loop.watch_pipe(self.got_pipe_data)
        self.log.debug('urwid.loop.watch_pipe() write_fd={0}'.format(self._write_fd))
        self.sevent = saltobj.ForkedSaltPipeWriter(self.args)
        self.sevent.pipe_loop(self._write_fd)

    def exit_on_q(self,input):
        if input in ('q', 'Q'):
            self.see_ya('q')

    def sig(self, signo,frame):
        self.hear_event('q')

    def run(self):
        signal.signal(signal.SIGINT, self.sig)
        self.loop.run()
        self.sevent.see_ya()

    def see_ya(self,*x):
        if len(x):
            self.log.debug("received signal={0}".format(x[0]))
        self.sevent.see_ya()
        raise urwid.ExitMainLoop()

    def status(self,status):
        self.status_txt.set_text(('banner', status))

    def hear_event(self, x):
        os.write( self._write_fd, x + '\xe1' )

    def handle_salt_event(self, event):
        self.log.debug('handle_salt_event()')
        self.events_listwalker.append( wrapper.Event( event ) )

    def handle_salt_data(self, data):
        self.log.debug('handle_salt_data(evno={0})'.format(data.get('_evno')))
        event = saltobj.classify_event( data )
        self.handle_salt_event( event )

    def got_pipe_data(self,data):
        if data:
            self._pdat+= data
        short = repr(self._pdat)
        if len(short) > 20:
            short = short[0:20] + '…'
        self.log.debug('got_pipe_data() len(_pdat)={0} _pdat={1}'.format(
            len(self._pdat, short)))
        while saltobj.RS in self._pdat:
            d1,_,d2 = self._pdatpartition(saltobj.RS)
            self.log.debug("  gpd() len(d1)={0} len(d2)={1}".format(
                len(d1), len(d2) ))
            self._pdat= d2
            self.got_event(d1)

    def got_event(self,data):
        if data.lower().strip() == 'q':
            self.see_ya('q')

        short = repr(data)
        if len(short) > 20:
            short = short[0:20] + '…'
        self.log.debug('got_event() len(data)={0} data={1}'.format(len(data), short))

        self.event_no += 1
        if self.event_no == 1: self.status(u'got event')
        else: self.status(u'got {0} events'.format(self.event_no))

        if data.startswith('json:'):
            try:
                self.handle_salt_data(json.loads(data[5:]))
            except Exception as e:
                self.log.warning("exception trying to handle json data: {0}".format(e))
