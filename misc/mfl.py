# coding: utf-8

import urwid.listbox
from urwid.monitored_list import MonitoredFocusList as pMFL

# /usr/lib/python2.7/site-packages/urwid/monitored_list.py

class MyFocusListMixin(object):
    def _set_focus(self, index):
        if not self: return
        index = index % len(self)
        super(MyFocusListMixin, self)._set_focus(index)

    focus = property(pMFL._get_focus, _set_focus)

    @property
    def cur(self):
        if not self:
            return
        return self[ self.focus ]

    @property
    def next(self):
        self.focus += 1
        return self.cur

    @property
    def prev(self):
        self.focus -= 1
        return self.cur

class MyFocusList(urwid.monitored_list.MonitoredFocusList, MyFocusListMixin):
    pass

class MySimpleFocusListWalker(urwid.listbox.SimpleFocusListWalker, MyFocusListMixin):
    pass
