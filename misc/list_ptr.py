
import urwid.monitored_list

# I think this might be partially re-inventing-the-wheel …
# isn't this what list walkers are for?

class ListWithPtr(urwid.monitored_list.MonitoredList):
    _pos = -1
    siv  = []

    def __init__(self, *a, **kw):
        super(ListWithPtr,self).__init__(*a, **kw)
        self._modified()

    def _modified(self):
        if not self:
            self._pos = -1
            while self.siv:
                self.siv.pop()

        elif not self.siv or self.siv[0] is not self.cur:
            while self.siv:
                self.siv.pop()
            self.siv.append(self.cur)
            
    @property
    def cur(self):
        try: return self[ self.pos ]
        except: pass

    @property
    def next(self):
        try: self.pos += 1
        except: pass
        self._modified()
        return self.cur

    @property
    def prev(self):
        try: self.pos -= 1
        except: pass
        self._modified()
        return self.cur

    @property
    def pos(self):
        try: return self._pos % len(self)
        except: pass

    @pos.setter
    def pos(self, v):
        self._pos = v
        self._modified()
        return self.pos

    def __repr__(self):
        p = self.pos
        return '[' + (' '.join([
            ('<{0}>' if i == p else '{0}').format(v) for i,v in enumerate(self)
        ])) + ']'
