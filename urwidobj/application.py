# coding: utf-8

import signal, os, json
import urwid

import misc
import saltobj
import wrapper
import command_map_extra
from pallet import get_pallet

class EventApplication(object):
    pallet = get_pallet('main')
    event_no = 0

    def __init__(self, args):
        self.args = args

        self._pdat= ''

        self.status_txt    = urwid.Text(('status', u"wating for events"))
        self.key_hints_txt = urwid.Text(('status', u''), align='right')
        self.log = misc.setup_file_logger(args, 'urwidobj.EventApplication')

        ############# OOM
        # I'm shocked how often urwid and/or the fork goes completely wonky and
        # newks the whole system until OOM rescues it.
        my_oom_adj = '/proc/{pid}/oom_score_adj'.format( pid=os.getpid() )
        if os.path.isfile(my_oom_adj):
            self.log.info("setting {0} to 1000".format(my_oom_adj))
            with open(my_oom_adj, 'w') as fh:
                fh.write('1000')
        ############# /OOM

        self.events = []
        self.events_listwalker = urwid.SimpleFocusListWalker(self.events)
        self.events_listbox = urwid.ListBox(self.events_listwalker)
        self.main_frame = urwid.Frame(
            self.events_listbox,
            footer=urwid.Columns([
                urwid.AttrMap(self.status_txt,    'status'),
                urwid.AttrMap(self.key_hints_txt, 'status'),
            ], min_width=20)
        )

        command_map_extra.add_vim_keys()
        command_map_extra.add_cisco_keys()

        self.page_stack = [self.events_listbox]

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

        self.show_cursor = urwid.escape.SHOW_CURSOR
        urwid.escape.SHOW_CURSOR = ''

        self._write_fd = self.loop.watch_pipe(self.got_pipe_data)
        self.log.debug('urwid.loop.watch_pipe() write_fd={0}'.format(self._write_fd))
        self.sevent = saltobj.ForkedSaltPipeWriter(self.args)
        self.sevent.pipe_loop(self._write_fd)

    def exit_on_q(self,input):
        self.log.debug('got keyboard input: {0}'.format(input))

        if input in ('left'):
            self.pop_page()

        elif input in ('q', 'Q', 'meta q', 'meta Q'):
            if not self.pop_page():
                self.see_ya('q')

    def sig(self, signo,frame):
        if signo in (signal.SIGINT,):
            self.exit_on_q('q')
        else:
            self.log.info("ignoring signal={0}".format(signo))

    def run(self):
        signal.signal(signal.SIGINT, self.sig)
        self.loop.run()
        self.sevent.see_ya()

    def see_ya(self,*x):
        self.loop.screen.write( self.show_cursor ) # urwid's ability to do this was disabled
        if len(x):
            self.log.debug("received signal={0}".format(x[0]))
        self.sevent.see_ya()
        raise urwid.ExitMainLoop()

    def status(self,status):
        self.status_txt.set_text(('status', status))

    def update_key_hints(self):
        body_widget = self.main_frame.body
        key_hints = body_widget.key_hints if hasattr(body_widget,'key_hints') else ''
        self.key_hints_txt.set_text( key_hints )

    def push_page(self, widget):
        if self.page_stack[-1] is not widget:
            self.page_stack.append(widget)
            self.main_frame.body = widget
            self.log.debug("push page={0}".format(widget))
            self.update_key_hints()
            return True
        self.log.debug("skipping push page={0} (already last on stack)".format(widget))
        return False

    def pop_page(self):
        l = len(self.page_stack)
        if l > 1:
            self.log.debug("popping page (depth={0})".format(l))
            self.page_stack.pop()
            self.main_frame.body = self.page_stack[-1]
            self.update_key_hints()
            return True
        self.log.debug("skipping pop page (depth={0})".format(l))
        return False

    def event_button_click(self, evw):
        self.log.debug('event_button_click(evw={0})'.format(evw))
        self.log.debug("main_frame.contents[body]={0}".format(self.main_frame.contents['body']))
        self.push_page( evw.viewer )

    def handle_salt_event(self, event):
        self.log.debug('handle_salt_event()')
        evw = wrapper.EventButton(event, self.event_button_click)
        for ev in self.events_listwalker:
            ev.update_short()
        self.events_listwalker.append(evw)
        gf1 = self.events_listwalker.get_focus()[1]
        gfn = self.events_listwalker.get_next(gf1)
        if gfn[0] is evw:
            self.events_listwalker.set_focus(gfn[1])

    def handle_salt_data(self, data):
        self.log.debug('handle_salt_data(evno={0})'.format(data.get('_evno')))
        event = saltobj.classify_event( data )
        self.handle_salt_event( event )

    def got_pipe_data(self,data):
        self.log.debug("got_pipe_data() {0} byte(s)".format(len(data)))
        if data:
            self._pdat+= data
        while saltobj.RS in self._pdat:
            d1,_,d2 = self._pdat.partition(saltobj.RS)
            self._pdat= d2
            self.got_event(d1)

    def got_event(self,data):
        if data.lower().strip() == 'q':
            self.see_ya('q')

        self.log.debug('got_event() {0} byte(s)'.format(len(data)))

        self.event_no += 1
        if self.event_no == 1: self.status(u'got event')
        else: self.status(u'got {0} events'.format(self.event_no))

        if data.startswith('json:'):
            try:
                self.handle_salt_data(json.loads(data[5:]))
            except Exception as e:
                self.log.warning("exception trying to handle json data: {0}".format(e))
