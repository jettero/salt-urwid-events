
import pytest
import note

@pytest.fixture
def note_events():
    return note.get_events()
