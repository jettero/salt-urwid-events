
from misc import MyFocusList
from urwid.listbox import SimpleFocusListWalker

def test_mfl():
    l = MyFocusList([1,2,3,4])
    assert l.focus == 0
    l.focus = -1
    assert l.focus == len(l)-1
    assert l.cur == 4
    assert l.next == 1
    assert l.next == 2
    assert l.next == 3
    assert l.next == 4
    assert l.next == 1
    assert l.prev == 4
    assert l.prev == 3
    assert l.prev == 2
    assert l.prev == 1
    assert l.prev == 4
    assert l.cur == 4
    assert l.cur == 4
    assert l.cur == 4

def test_auto_follow():
    l = MyFocusList([1,2,3,4])
    l.focus = -1
    assert l.cur == 4
    l.append(5)
    assert l.cur == 4
    l.auto_follow = True # turn on auto follow
    l.append(6)          # since we're not on the last item
    assert l.cur == 4    # we shouldn't follow here
    l.focus = -1
    assert l.cur == 6
    l.append(7)
    assert l.cur == 7 # we should have followed this time though

def test_babysit_list():
    sflw = SimpleFocusListWalker([])
    mfl = MyFocusList([1,2,3,4], babysit_list=sflw)

    assert len(sflw) == 1 and sflw[0] == mfl.cur
