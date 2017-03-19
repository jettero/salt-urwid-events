# encoding: utf-8

import saltobj.event
import urwid
import command_map_extra
import logging

from misc.xlateansi import xlate_ansi, format_code
from misc import ListWithPtr

class AnsiableText(urwid.Text):
    def __init__(self, *a,**kw):
        self.log = logging.getLogger(self.__class__.__name__)
        super(AnsiableText,self).__init__(*a,**kw)

    def set_text(self,text):
        if not isinstance(text,(tuple,list)):
            text = xlate_ansi(text)
        super(AnsiableText,self).set_text( text )

class ColumnText(urwid.Text): 
    def __init__(self,text):
        super(ColumnText,self).__init__(text, wrap='clip', align='left')

class EventListWalker(urwid.SimpleFocusListWalker):
    pass

class EventButton(urwid.Button):
    _viewer = None

    def __init__(self, event, callback):
        self.log = logging.getLogger(self.__class__.__name__)
        if not isinstance(event,saltobj.event.Event):
            raise TypeError("urwidobj.wrapper.Event only understands saltobj.event.Event objects")
        self.event = event
        super(EventButton,self).__init__(u' ')
        urwid.connect_signal(self, 'click', callback)

        evc = self.event.columns

        columns = [('fixed', 1, self._label)]
        columns.extend([ ColumnText(c) for c in evc ])

        self._w = urwid.Columns( columns, min_width=True, dividechars=1 )
        command_map_extra.add_vim_right_activate(self)

    def render(self, size, focus=False):
        self._label.set_text( u'·' if focus else u' ' )
        return super(EventButton,self).render(size,focus=focus)

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
    view = None

    def __init__(self,event):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event = event
        self.outputs = ListWithPtr()
        self.outputs.siv = urwid.SimpleFocusListWalker([])
        self.outputs.append( CodeViewer(event) )
        if hasattr(event, 'outputter'):
            self.outputs.append( OutputterViewer(event) )
        super(EventViewer, self).__init__(self.outputs.siv)
        command_map_extra.add_cisco_pager_keys(self)

    def key_hints_signal(self, their_cb):
        urwid.connect_signal(self, 'key-hints', their_cb)

    @property
    def key_hints(self):
        kh = self.outputs.cur.key_hints
        kh = kh + ' [m]ode' if kh else '[m]ode'
        self.log.debug("built new key-hints: «{0}»".format(kh))
        return kh

    def keypress(self,*a,**kw):
        key = super(EventViewer,self).keypress(*a,**kw)

        if key and self.key_hints: # if key is true, super() didn't handle the keypress
            if key in ('m',):
                self.outputs.next
                self.log.debug('swapping mode {0} {1}'.format(self.outputs.pos,self.outputs.siv))
                return # we handled the keystroke

            else:
                # XXX: this is the wrong way to do this, but I don't know how the key signals work
                # so I'm re-inventing the wheel until I later figure it out (never?)
                key = self.outputs.cur.handle_key(key)
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
