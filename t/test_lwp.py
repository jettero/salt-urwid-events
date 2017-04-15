
from misc.list_ptr import ListWithPtr

def test_lwp():
    lwp1 = ListWithPtr([1,2,3,4])
    assert lwp1.pos == 0
    lwp1.pos = -1
    assert lwp1.pos == len(lwp1)-1
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
