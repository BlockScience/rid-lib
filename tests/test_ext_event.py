from rid_lib import RID
from rid_lib.ext import Event, EventType, Manifest

def test_event_equivalency():
    rid = RID.from_string("test:rid")
    m = Manifest.generate(rid, {})

    e1 = Event(rid, EventType.NEW)
    e1r = Event.from_json(e1.to_json())
    assert e1 == e1r
    assert e1.to_json() == e1r.to_json()

    e2 = Event(rid, EventType.UPDATE, m)
    e2r = Event.from_json(e2.to_json())
    assert e2 == e2r
    assert e2.to_json() == e2r.to_json()