# encoding: utf-8

import saltobj.event
import urwid
import command_map_extra
import logging

from misc.xlateansi import xlate_ansi, format_code
from misc import MyFocusList
from urwid.listbox import SimpleFocusListWalker

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
        try: recompute = kw.pop('recompute')
        except: recompute = False
        if not recompute and self.minor_max:
            r = (self.minor_max,1)
            return r
        return super(ColumnText,self).pack(*a,**kw)

class EventListWalker(MyFocusList,urwid.SimpleFocusListWalker):
    minor_max = 30
    auto_follow = True

    def __init__(self,*a,**kw):
        if not a:
            a = ([],)
        super(EventListWalker,self).__init__(*a,**kw)
        self.log = logging.getLogger(self.__class__.__name__)

        if a[0]:
            self._modified()

    def _modified(self):
        minor_maxes = []

        for item in self:
            if isinstance(item, EventButton):
                c = [ x.pack((self.minor_max,),recompute=True)[0] for x in item.mm_widget_list[:-1] ]
                for i,l in enumerate(c):
                    if i >= len(minor_maxes):
                        minor_maxes.append(l)
                    elif minor_maxes[i] < l:
                        minor_maxes[i] = l

        did_something = False
        for item in self:
            wl = item.mm_widget_list
            if isinstance(item, EventButton):
                for i,m in enumerate(minor_maxes):
                    if wl[i].minor_max != m:
                        did_something = True
                        wl[i].minor_max = m
                        wl[i]._invalidate()
                        did_something = True

        if did_something:
            for item in self:
                item._invalidate()

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

    @property
    def mm_widget_list(self):
        return [ w for w in self._w.widget_list if isinstance(w,ColumnText) ]

    def set_focused(self):
        self._label.set_text( u'*' )

    def set_unfocused(self):
        self._label.set_text( u' ' )

    @property
    def mm_widget_list(self):
        return self._w.widget_list[1:]

    def viewer(self):
        if not self._viewer:
            self._viewer = EventViewer(self.wrapped)
        return self._viewer

class JobListWalker(EventListWalker):
    def updated(self):
        for item in self:
            item.updated()

class JobButton(EventButton):
    _req_type = saltobj.event.Job
    pile = below = grid_flow = None

    def __init__(self, *a, **kw):
        super(JobButton,self).__init__(*a, **kw)
        self._main = self._w

    @property
    def mm_widget_list(self):
        wl = []
        todo = [ self._w ]
        while todo:
            top = todo.pop()
            if hasattr(top,'widget_list'):
                for w in top.widget_list:
                    if isinstance(w,ColumnText):
                        wl.append( w )
                    else:
                        todo.append( w )
        return wl

    def set_unfocused(self):
        self.log.debug("set_unfocused() jid={}".format(self.wrapped.jid if hasattr(self.wrapped,'jid') else '??'))
        super(JobButton,self).set_unfocused()
        evc = self.wrapped.columns
        columns = [('fixed', 1, self._label)] + [ ('pack',ColumnText(c)) for c in evc[:-1] ]
        columns.append(ColumnText(evc[-1]))
        self.grid_flow = None
        self.below = None
        self.pile = None
        self._w = urwid.Columns( columns, min_width=True, dividechars=1 )
        self._invalidate()

    def set_focused(self):
        self.log.debug("set_focused() jid={}".format(self.wrapped.jid if hasattr(self.wrapped,'jid') else '??'))
        super(JobButton,self).set_focused()
        evc = self.wrapped.columns
        more_columns = [ ('pack',ColumnText(c)) for c in evc[:-1] ]
        more_columns.append(ColumnText(evc[-1]))
        self.grid_flow = urwid.GridFlow([urwid.Text('<>')], 1, 2, 0, 'left' )
        self.below = urwid.Columns([ ('fixed', 1, urwid.Text('')), self.grid_flow ])
        self.pile = urwid.Pile([
            urwid.Columns( more_columns, min_width=True, dividechars=1 ),
        ])
        columns = [('fixed', 1, self._label), self.pile]
        self._w = urwid.Columns( columns, min_width=True, dividechars=1 )
        self._invalidate()
        self._update_grid_flow()

    def _update_grid_flow(self):
        self.log.debug('_update_grid_flow()')
        if self.grid_flow:
            details = self.wrapped.job_detail
            self.log.debug('_update_grid_flow() details={}'.format(details))
            if details:
                m = 0
                for h in details:
                    lh = len(h[0])
                    if lh > m:
                        m = lh
                self.log.debug('_update_grid_flow() m={}'.format(m))

                def _frob_host(x):
                    host = x[0]
                    statuses = x[1:]
                    if 'ayt' in statuses:
                        return ('ayt', host)
                    p = []
                    if 'rc_ok' in statuses:
                        p.append('rc_ok')
                    elif 'rc_bad' in statuses:
                        p.append('rc_bad')
                    if 'changes' in statuses:
                        p.append('changes')
                    if not p:
                        return host
                    return ('-'.join(p), host)

                hosts = [( urwid.Text(_frob_host(x)), ('given',len(x[0])) ) for x in details ]

                #self.grid_flow.cell_width = m
                self.grid_flow.contents[:] = hosts
                if len(self.pile.contents) == 1:
                    self.pile.contents.append( (self.below, ('weight', 1)) )
                    self.log.debug('_update_grid_flow() append pile')
                self._invalidate()
            else:
                if len(self.pile.contents) > 1:
                    self.pile.contents.pop()
                    self._invalidate()
                    self.log.debug('_update_grid_flow() pop pile')

    @property
    def jid(self):
        return self.wrapped.jid

    def viewer(self, ev_click_cb):
        elw = EventListWalker([ EventButton(x, ev_click_cb) for x in self.wrapped.all_events ])
        lb = urwid.ListBox( elw )
        return lb

    def updated(self):
        evc = self.wrapped.columns
        wl  = self.mm_widget_list
        assert( len(evc) == len(wl) )

        for i in range(len(evc)):
            # should we check to see if the text really changed before we change it?
            wl[i].set_text( evc[i] )

        self._update_grid_flow()

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
        self.output_lw = SimpleFocusListWalker([])
        self.outputs   = MyFocusList([ CodeViewer(event) ], auto_follow=1, babysit_list = self.output_lw)
        if hasattr(event, 'outputter'):
            self.outputs.append( OutputterViewer(event) )
        super(EventViewer, self).__init__(self.output_lw)
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
                self.log.debug('swapping mode {0}'.format(self.outputs))
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
