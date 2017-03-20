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

    max_events = 100

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

        self.events_listwalker = wrapper.EventListWalker()
        self.events_listbox    = urwid.ListBox(self.events_listwalker)

        self.jidcollector    = saltobj.JidCollector()
        self.jobs_listwalker = wrapper.JobListWalker()
        self.jobs_listbox    = urwid.ListBox(self.jobs_listwalker)

        self.jidcollector.on_change(self.deal_with_job_changes)

        start_page = self.jobs_listbox
        # self.events_listbox

        status_line = urwid.Columns([
            urwid.AttrMap(urwid.Padding(self.status_txt, left=1),     'status'),
            urwid.AttrMap(urwid.Padding(self.key_hints_txt, right=1), 'status'),
        ], min_width=20)

        self.log.debug("TERM={0} TMUX={1}".format(os.environ.get('TERM'), os.environ.get('TMUX')))
        if os.environ.get('TERM') == 'screen':
            self.log.debug('attempting to address LR-corner issue in tmux terminals')
            status_line = urwid.Padding(status_line, right=1)

        self.main_frame = urwid.Frame( start_page, footer=status_line)

        command_map_extra.add_vim_keys()

        self.page_stack = [start_page]

        self.update_key_hints()

        _a   = (self.main_frame,self.pallet,)
        _kw = { 'unhandled_input': self.keypress }

        self.curses_mode = False

        # try:
        #     self.log.debug('trying to use curses')
        #     from urwid import curses_display
        #     _kw['screen'] = curses_display.Screen()
        #     self.curses_mode = True
        # except Exception as e:
        #     self.log.debug("self.loop exception: {0}".format(e))
        #     self.log.info("failed to use curses, trying the default instead")

        self.loop = urwid.MainLoop(*_a, **_kw)

        # OLD0319: this was needed when the event buttons had selectable icons, which 
        #          always contain a cursor for some reason (why?); this has a counterpart
        #          cruft-comment the same OLD0319 comment tag
        # if not self.curses_mode:
        #     self.show_cursor = urwid.escape.SHOW_CURSOR
        #     urwid.escape.SHOW_CURSOR = ''

        self._write_fd = self.loop.watch_pipe(self.got_pipe_data)
        self.log.debug('urwid.loop.watch_pipe() write_fd={0}'.format(self._write_fd))
        self.sevent = saltobj.ForkedSaltPipeWriter(self.args)

        self.sevent.pipe_loop(self._write_fd)

    def save_event(self):
        gf0 = self.events_listwalker.get_focus()[0]
        evr = gf0.event.raw
        evn = evr.get('_evno', 999)
        fname = '/tmp/{0}.event-{1:04d}.json'.format(os.getpid(), evn)
        with open(fname, 'w') as fh:
            fh.write( json.dumps(evr, indent=2) )

        if 'SUDO_GID' in os.environ and 'SUDO_UID' in os.environ:
            try:
                uid = int(os.environ.get('SUDO_UID'))
                gid = int(os.environ.get('SUDO_GID'))
                os.chown(fname, uid,gid)
            except Exception as e:
                self.log.info('tried to chown({0},{1},{2}) but failed: {3}'.format(
                    fname,os.envrion.get('SUDO_UID'),os.environ.get('SUDO_GID'),e))

        self.status("wrote event to {0}".format(fname))

    def keypress(self,key):
        self.log.debug('got keyboard input: {0}'.format(key))

        if key in ('left','h'):
            self.pop_page()

        elif key in ('s',):
            self.save_event()

        elif key in ('q', 'Q', 'meta q', 'meta Q'):
            if not self.pop_page():
                self.see_ya('q')

    def sig(self, signo,frame):
        if signo in (signal.SIGINT,):
            self.keypress('q')
        else:
            self.log.info("ignoring signal={0}".format(signo))

    def run(self):
        self.log.debug('attaching SIGINT handler')
        signal.signal(signal.SIGINT, self.sig)
        self.log.debug('running mainloop')
        self.loop.run()
        self.log.debug('mainloop run ended, saying goodbye')
        self.sevent.see_ya()

    def see_ya(self,*x):
        # OLD0319
        # if not self.curses_mode:
        #     # we disable show_cursor in raw_display (but not in curses mode)
        #     # so if we're in raw display, we have to show cursor again at the end
        #     self.loop.screen.write( self.show_cursor )
        if len(x):
            self.log.debug("received signal={0}".format(x[0]))
        self.sevent.see_ya()
        raise urwid.ExitMainLoop()

    def status(self,status):
        self.status_txt.set_text(('status', status))

    def update_key_hints(self):
        body_widget = self.main_frame.body
        key_hints = ['[s]ave-event']
        if hasattr(body_widget,'key_hints'):
            key_hints.append(body_widget.key_hints)
        key_hints = ' '.join(key_hints)
        self.key_hints_txt.set_text( key_hints )
        self.log.debug("updating key hints")

    def push_page(self, widget):
        if self.page_stack[-1] is not widget:
            if hasattr(widget, 'key_hints_signal'):
                widget.key_hints_signal( self.update_key_hints )
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

    def deal_with_job_changes(self, jitem, actions):
        for jbutt in self.jobs_listwalker:
            if jbutt.wrapped is jitem:
                jbutt.updated()
                self.jobs_listwalker.updated()
                return

        self.jobs_listwalker.append( wrapper.JobButton(jitem, lambda: True) )

    def event_button_click(self, evw):
        self.log.debug('event_button_click(evw={0})'.format(evw))
        self.log.debug("main_frame.contents[body]={0}".format(self.main_frame.contents['body']))
        self.push_page( evw.viewer )

    def handle_salt_event(self, event):
        self.log.debug('handle_salt_event()')
        self.jidcollector.examine_event(event)
        evw = wrapper.EventButton(event, self.event_button_click)
        self.events_listwalker.append(evw)
        while len(self.events_listwalker) > self.max_events:
            self.events.listwalker.pop(0)
        gf1 = self.events_listwalker.get_focus()[1]
        gfn = self.events_listwalker.get_next(gf1)
        try: self.log.debug(' gfn[0].evno={0} is evw.evno={1} ?'.format(gfn[0].evno,evw.evno))
        except: self.log.debug('considering focus update')
        if gfn[0] is evw:
            self.log.debug(' update_focus(gfn[1]={0})'.format(gfn[1]))
            self.events_listwalker.set_focus(gfn[1])
        else:
            self.log.debug(' leave focus alone')

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
                self.log.exception("exception trying to handle json data")
