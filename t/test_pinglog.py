
import saltobj

def test_classify(pinglog_json):
    for evj in pinglog_json:
        ev = saltobj.classify_event( evj )
        assert isinstance( ev, (saltobj.event.Event) )
