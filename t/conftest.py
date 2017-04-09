
import pytest
import saltobj

@pytest.fixture
def pinglog_json():
    return list(saltobj.read_event_file('t/_ping.log'))
