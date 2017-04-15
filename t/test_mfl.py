
from misc.mfl import MyFocusList, MySimpleFocusListWalker

def test_mfl(test_class=MyFocusList):
    l = test_class([1,2,3,4])
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

def test_msflw():
    test_mfl( MySimpleFocusListWalker )

