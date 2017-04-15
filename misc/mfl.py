# coding: utf-8

import urwid.monitored_list
import urwid.listbox

# /usr/lib/python2.7/site-packages/urwid/monitored_list.py

class MyFocusListMixin(object):
    @property
    def cur(self):
        if not self:
            return
        return self[ self._focus ]

    @property
    def next(self):
        if not self: return
        self.pos += 1
        return self.cur

    @property
    def prev(self):
        if not self: return
        self.pos -= 1
        return self.cur

    @property
    def pos(self):
        if not self: return
        return self._focus % len(self)

    @pos.setter
    def pos(self, v):
        if not self: return
        self._focus = v % len(self)

class MyFocusList(urwid.monitored_list.MonitoredFocusList, MyFocusListMixin):
    pass

class MySimpleFocusListWalker(urwid.listbox.SimpleFocusListWalker, MyFocusListMixin):
    pass
