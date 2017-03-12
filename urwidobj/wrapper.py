import saltobj.event
import urwid
import command_map_extra
import logging

from misc.xlateansi import xlate_ansi, format_code

class AnsiableText(urwid.Text):
    def __init__(self, *a,**kw):
        self.log = logging.getLogger(self.__class__.__name__)
        super(AnsiableText,self).__init__(*a,**kw)

    def set_text(self,text):
        if not isinstance(text,(tuple,list)):
            text = xlate_ansi(text)
        super(AnsiableText,self).set_text( text )

class EventButton(urwid.Button):
    _viewer = None

    def __init__(self, event, callback):
        self.log = logging.getLogger(self.__class__.__name__)
        if not isinstance(event,saltobj.event.Event):
            raise TypeError("urwidobj.wrapper.Event only understands saltobj.event.Event objects")
        self.event = event
        super(EventButton,self).__init__('')
        urwid.connect_signal(self, 'click', callback)
        cursor_pos_in_button = 0
        attr_map  = None
        focus_map = 'selected'
        self._si = urwid.SelectableIcon(event.short, cursor_pos_in_button)
        self._w = urwid.AttrMap(self._si, attr_map, focus_map)
        command_map_extra.add_vim_right_activate(self)

    def update_short(self):
        if self.event.short != self._si.text:
            self._si.set_text( self.event.short )

    @property
    def viewer(self):
        if not self._viewer:
            self._viewer = EventViewer(self.event)
        return self._viewer

class CodeViewer(AnsiableText):
    def __init__(self,event):
        super(CodeViewer,self).__init__( format_code(event.long) )

    @property
    def key_hints(self):
        pass

    def handle_key(self, key):
        return key

class OutputterViewer(AnsiableText):
    def __init__(self,event):
        self.event = event
        super(OutputterViewer,self).__init__( event.outputter )

    @property
    def key_hints(self):
        if hasattr(self.event, 'outputter_opts'):
            ret = []
            for a in self.event.outputter_opts:
                ret.append(a['fmt'].format( a['cb'](*a['args']) ))
            return ' '.join(ret)

    def handle_key(self, key):
        for a in self.event.outputter_opts:
            if a['key'] == key:
                # srsly?
                # XXX this is a total mess. Handlers for this crap should all be moved to a mixin for
                # both OutputterViewer (if it lives through the refactor) and the poor Return object
                # in saltobj/event.py
                a['cb'](*(a['args'] + [a['choices']]))
                self.set_text( self.event.outputter )
                return
        return key

class EventViewer(urwid.ListBox):
    key_hints = ''
    opos = 0
    view = None

    def __init__(self,event):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event = event
        self.outputs = [ CodeViewer(event) ]
        if hasattr(event, 'outputter'):
            self.outputs.append( OutputterViewer(event) )
        self.opos = len( self.outputs ) -1
        self.goto_view()
        lw = urwid.SimpleFocusListWalker(self.view)
        super(EventViewer, self).__init__(lw)
        command_map_extra.add_cisco_pager_keys(self)

    def goto_view(self, pos=None):
        if pos is None:
            pos = self.opos
        if not self.view:
            self.view = [self.outputs[pos]]
        elif self.view[0] is not self.outputs[pos]:
            self.view.append(self.outputs[pos])
            while len(self.view) > 1:
                self.view.pop(0)
        urwid.emit_signal(self, 'key-hints')

    def key_hints_signal(self, their_cb):
        urwid.connect_signal(self, 'key-hints', their_cb)

    @property
    def key_hints(self):
        kh = self.view[0].key_hints
        kh = kh + ' [m]ode' if kh else '[m]ode'
        self.log.debug("built new key-hints: {0}".format(kh))
        return kh + ' '

    def keypress(self,*a,**kw):
        key = super(EventViewer,self).keypress(*a,**kw)

        if key and self.key_hints: # if key is true, super() didn't handle the keypress
            if key in ('m',):
                self.log.debug('swapping mode {0}[({1}+1)%len]'.format(self.outputs,self.opos))
                self.opos = (self.opos + 1) % len(self.outputs)
                self.long_txt.set_text( self.outputs[self.opos](self.event) )
                return # we handled the keystroke

            else:
                # XXX: this is the wrong way to do this, but I don't know how the key signals work
                # so I'm re-inventing the wheel until I later figure it out (never?)
                key = self.view[0].handle_key(key)
                if not key:
                    # if we handled the key, we should update key hints too
                    urwid.emit_signal(self, 'key-hints')

        return key # returning this means we didn't deal with it

urwid.register_signal(EventViewer,'key-hints')

### never finished this thought, but seems like there's decent progress here
# class JobItem(urwid.Text):
#     def __init__(self, jitem):
#         self.jitem = jitem
#         super(JobItem,self).__init__( ('jitem', jitem.jid) )

#     def __eq__(self, other):
#         return other.jitem == self.jitem

# class JobList(uriwid.ListBox):
#     def __init__(self):
#         self.jc = saltobj.jidcollector()
#         self.jc.on_change(self._jc_update)
#         self.events = []
#         self.walker = urwid.SimpleListWalker(self.events)
#         super(JobList,self).__init__( self.walker )

#     def _jc_update(self, jitem, actions):
#         if 'new-jid' in actions:
#             if jitem not in self.events:
#                 self.events.append(JobItem(jitem))
#         # TODO: append-event, add-expected, remove-expected, add-returned
