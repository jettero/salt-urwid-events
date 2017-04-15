# coding: utf-8

import urwid.listbox
from urwid.monitored_list import MonitoredFocusList as pMFL

# /usr/lib/python2.7/site-packages/urwid/monitored_list.py

class MyFocusListMixin(urwid.monitored_list.MonitoredFocusList):
    auto_follow = False

    def __init__(self, *a, **kw):
        if 'auto_follow' in kw: self.auto_follow = bool(kw.pop('auto_follow'))
        if 'follow' in kw:      self.auto_follow = bool(kw.pop('follow'))
        if 'focus' in kw and kw['focus'] == -1:
            self.auto_follow = True
        super(MyFocusListMixin, self).__init__(*a, **kw)

    def _adjust_focus_on_contents_modified(self, slc, new_items=()):
        focus = super(MyFocusListMixin, self)._adjust_focus_on_contents_modified(slc, new_items=new_items)
        if self.auto_follow and new_items:
            if focus == len(self)-1:
                focus += len(new_items)
        return focus

    def _set_focus(self, index):
        if not self: return
        index = index % len(self)
        pMFL._set_focus(self, index)

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

class MyFocusList(MyFocusListMixin):
    pass

class MySimpleFocusListWalker(MyFocusListMixin, urwid.listbox.SimpleFocusListWalker):
    pass
