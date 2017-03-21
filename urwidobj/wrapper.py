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
    minor_max = 0

    def __init__(self,text):
        super(ColumnText,self).__init__(text, wrap='clip', align='left')

    def pack(self,*a,**kw):
        if self.minor_max:
            r = (self.minor_max,1)
            return r
        return super(ColumnText,self).pack(*a,**kw)

class EventListWalker(urwid.SimpleFocusListWalker):
    minor_max = 50

    def __init__(self,*a,**kw):
        if not a:
            a = ([],)
        super(EventListWalker,self).__init__(*a,**kw)
        self.log = logging.getLogger(self.__class__.__name__)

        if a[0]:
            self._modified()

    def updated(self):
        self._modified()

    def _modified(self):
        minor_maxes = []

        for item in self:
            if isinstance(item, EventButton):
                c = [ x.pack((self.minor_max,))[0] for x in item._w.widget_list[1:-1] ]
                for i,l in enumerate(c):
                    if i >= len(minor_maxes):
                        minor_maxes.append(l)
                    elif minor_maxes[i] < l:
                        minor_maxes[i] = l

        did_something = False
        for item in self:
            if isinstance(item, EventButton):
                wl = item._w.widget_list
                for i,m in enumerate(minor_maxes):
                    if wl[i+1].minor_max == 0:
                        did_something = True
                    wl[i+1].minor_max = m

        if did_something:
            for item in self:
                if isinstance(item, EventButton):
                    for w in item._w.widget_list:
                        w._invalidate()

        super(EventListWalker,self)._modified()

class EventButton(urwid.Button):
    _viewer = None
    _req_type = saltobj.event.Event

    def __init__(self, in_obj, callback):
        self.log = logging.getLogger(self.__class__.__name__)
        if not isinstance(in_obj,self._req_type):
            raise TypeError("wrapped object type mismatch")
        self.wrapped = in_obj
        super(EventButton,self).__init__(u' ')
        urwid.connect_signal(self, 'click', callback)

        evc = self.wrapped.columns
        columns = [('fixed', 1, self._label)] + [ ('pack',ColumnText(c)) for c in evc[:-1] ]
        columns.append(ColumnText(evc[-1]))

        self._w = urwid.Columns( columns, min_width=True, dividechars=1 )
        command_map_extra.add_vim_right_activate(self)

        self.evno = 999
        if hasattr(self.wrapped,'raw') and '_evno' in self.wrapped.raw:
            self.evno = self.wrapped.raw.get('_evno',999)

        elif hasattr(self.wrapped,'jid'):
            self.evno = self.wrapped.jid

    def render(self, size, focus=False):
        self._label.set_text( u'·' if focus else u' ' )
        return super(EventButton,self).render(size,focus=focus)

    def viewer(self):
        if not self._viewer:
            self._viewer = EventViewer(self.wrapped)
        return self._viewer

class JobListWalker(EventListWalker):
    pass

class JobButton(EventButton):
    _req_type = saltobj.event.Job

    @property
    def jid(self):
        return self.wrapped.jid

    def viewer(self, ev_click_cb):
        elw = EventListWalker([ EventButton(x, ev_click_cb) for x in self.wrapped.all_events ])
        lb = urwid.ListBox( elw )
        return lb

    def updated(self):
        evc = self.wrapped.columns
        wl  = self._w.widget_list
        assert( len(evc)+1 == len(wl) )

        for i,j in [ (i,i+1,) for i in range(len(evc)) ]:
            # should we check to see if the text really changed before we change it?
            wl[j].set_text( evc[i] )

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
