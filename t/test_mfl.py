
from misc.mfl import MyFocusList

def test_mfl():
    lwp1 = MyFocusList([1,2,3,4])
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
