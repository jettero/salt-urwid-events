# coding: utf-8

import re, argparse

class Matcher(object):
    m = None
    p = None

    def __init__(self, pattern):
        self.p = pattern
        self.re = re.compile(pattern)

    @property
    def sub(self, s, r):
        return self.re.sub

    def match(self, blah):
        self.m = self.re.match(blah)
        return self

    def search(self, blah):
        self.m = self.re.search(blah)
        return self

    def group(self, i):
        if self.m:
            return self.m.group(i)

    def groups(self):
        if self.m:
            return self.m.groups()

    def __bool__(self):
        return bool(self.m)
    __nonzero__=__bool__

    def __repr__(self):
        b = 'Matcher<{0}>'.format(self.p)
        if self.m:
            g = self.groups()
            if g: b += ':true {0}'.format(', '.join(g))
            else: b += ':true'
        else:
            b += ':false'
        return b
