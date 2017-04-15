# coding: utf-8

import urwid.monitored_list

# /usr/lib/python2.7/site-packages/urwid/monitored_list.py

class MyFocusList(urwid.monitored_list.MonitoredFocusList):
    auto_follow = False
    babysit_list = None

    def __init__(self, *a, **kw):
        set_focus = None
        if 'babysit' in kw:
            self.babysit_list = kw.pop('babysit')
        if 'auto_follow' in kw:
            self.auto_follow = bool(kw.pop('auto_follow'))
        if 'follow' in kw:
            self.auto_follow = bool(kw.pop('follow'))
        if 'focus' in kw:
            set_focus = kw.pop('focus')
        super(MyFocusList, self).__init__(*a, **kw)
        if set_focus is not None:
            if set_focus == -1:
                self.auto_follow = True
            self.focus = set_focus
        self._modified()

    def _modified(self):
        if self.babysit_list is not None:
            if self:
                self.babysit_list[:] = [ self.cur ]
            else:
                self.babysit_list[:] = []

    def _adjust_focus_on_contents_modified(self, slc, new_items=()):
        focus = super(MyFocusList, self)._adjust_focus_on_contents_modified(slc, new_items=new_items)
        if self.auto_follow and new_items:
            if focus == len(self)-1:
                focus += len(new_items)
        return focus

    def _set_focus(self, index):
        if not self: return
        index = index % len(self)
        super(MyFocusList,self)._set_focus(index)

    def _get_focus(self):
        return super(MyFocusList,self)._get_focus()

    focus = property(_get_focus, _set_focus)

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
