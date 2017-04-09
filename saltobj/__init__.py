
from event import JidCollector, classify_event
from forkedsalt import ForkedSaltPipeWriter, RS

def read_event_file(fname):
    fspw = ForkedSaltPipeWriter(replay_file=fname, replay_only=True)
    while True:
        evj = fspw.next()
        if evj: yield evj
        else: break

def classify_event_file(fname):
    for evj in read_event_file(fname):
        yield classify_event(evj)
