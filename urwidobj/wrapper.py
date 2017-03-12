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

class EventViewer(urwid.ListBox):
    key_hints = ''
    opos = 0

    def __init__(self,event):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event = event
        self.outputs = [ lambda e: format_code(e.long) ]
        if hasattr(event, 'outputter'):
            self.key_hints = '[m]ode '
            self.outputs.append( lambda e: e.outputter )
        self.long_txt = AnsiableText( self.outputs[-1](self.event) )
        self.opos = len( self.outputs ) -1
        lw = urwid.SimpleFocusListWalker([self.long_txt])
        super(EventViewer, self).__init__(lw)
        command_map_extra.add_cisco_pager_keys(self)

    def keypress(self,*a,**kw):
        key = super(EventViewer,self).keypress(*a,**kw)

        if key and self.key_hints: # if key is true, super() didn't handle the keypress
            if key in ('m',):
                self.log.debug('swapping mode {0}[({1}+1)%len]'.format(self.outputs,self.opos))
                self.opos = (self.opos + 1) % len(self.outputs)
                self.long_txt.set_text( self.outputs[self.opos](self.event) )
                return # we handled the keystroke

        return key # returning this means we didn't deal with it

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
