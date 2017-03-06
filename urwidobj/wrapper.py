import saltobj.event
import urwid
import command_map_vim
import logging

class EventButton(urwid.Button):
    _viewer = None

    def __init__(self, event, callback):
        if not isinstance(event,saltobj.event.Event):
            raise TypeError("urwidobj.wrapper.Event only understands saltobj.event.Event objects")
        self.event = event
        super(EventButton,self).__init__('')
        urwid.connect_signal(self, 'click', callback)
        cursor_pos_in_button = 0
        attr_map  = None
        focus_map = 'selected'
        self._w  = urwid.AttrMap(urwid.SelectableIcon(event.short, cursor_pos_in_button), attr_map, focus_map)
        command_map_vim.add_right_activate(self)

    @property
    def viewer(self):
        if not self._viewer:
            self._viewer = EventViewer(self.event)
        return self._viewer

class EventViewer(urwid.ListBox):
    def __init__(self,event):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event = event

        if hasattr(event, 'outputter'):
            self.key_hints = '[f]ormat-{0} [r]aw-json'.format(self.event.dat.get('out','nested'))
            self.long_txt = urwid.Text(self.event.outputter)
        else:
            self.key_hints = ''
            self.long_txt = urwid.Text(self.event.long)

        lw = urwid.SimpleFocusListWalker([self.long_txt])
        super(EventViewer, self).__init__(lw)

    def keypress(self,*a,**kw):
        key = super(EventViewer,self).keypress(*a,**kw)

        if key and self.key_hints: # if key is true, super() didn't handle the keypress
            if key in ('r',):
                self.log.debug('setting raw output')
                self.long_txt.set_text( self.event.long )
                return # we handled the keystroke

            if key in ('f',):
                self.log.debug('setting formatted output')
                self.long_txt.set_text( self.event.outputter )
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
