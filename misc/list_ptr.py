
class ListWithPtr(list):
    _pos = -1

    @property
    def cur(self):
        try: return self[ self.pos ]
        except: pass

    @property
    def next(self):
        try: self.pos += 1
        except: pass
        return self.cur

    @property
    def prev(self):
        try: self.pos -= 1
        except: pass
        return self.cur

    @property
    def pos(self):
        try: return self._pos % len(self)
        except: pass

    @pos.setter
    def pos(self, v):
        self._pos = v
        return self.pos

    def __repr__(self):
        p = self.pos
        return '[' + (' '.join([
            ('<{0}>' if i == p else '{0}').format(v) for i,v in enumerate(self)
        ])) + ']'
