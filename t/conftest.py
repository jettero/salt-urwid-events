
import pytest
import saltobj

def _replay_file(fname):
    fspw = saltobj.ForkedSaltPipeWriter(replay_file=fname, replay_only=True)
    ret = []
    evj = fspw.next()
    while evj:
        ret.append(evj)
        evj = fspw.next()
    return ret

@pytest.fixture
def pinglog_json():
    return _replay_file('t/_ping.log')
