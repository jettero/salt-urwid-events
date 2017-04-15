
from misc.mfl import MyFocusList, MySimpleFocusListWalker

def test_mfl(test_class=MyFocusList):
    lwp1 = test_class([1,2,3,4])
    assert lwp1.focus == 0
    lwp1.focus = -1
    assert lwp1.focus == len(lwp1)-1
    assert lwp1.cur == 4
    assert lwp1.next == 1
    assert lwp1.next == 2
    assert lwp1.next == 3
    assert lwp1.next == 4
    assert lwp1.next == 1
    assert lwp1.prev == 4
    assert lwp1.prev == 3
    assert lwp1.prev == 2
    assert lwp1.prev == 1
    assert lwp1.prev == 4
    assert lwp1.cur == 4
    assert lwp1.cur == 4
    assert lwp1.cur == 4

def test_msflw():
    test_mfl( MySimpleFocusListWalker )

