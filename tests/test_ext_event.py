import pytest
from rid_lib import RID

from rid_lib.ext import RID_EXT_ENABLED
if RID_EXT_ENABLED:
    from rid_lib.ext import Event, EventType, Manifest


@pytest.mark.skipif(not RID_EXT_ENABLED, reason="Missing rid-lib ext dependencies")
def test_event_equivalency():
    rid = RID.from_string("test:rid")
    m = Manifest.generate(rid, {})

    e1 = Event(rid=rid, event_type=EventType.NEW)
    e1r = Event.model_validate(e1.model_dump())
    assert e1 == e1r
    assert e1.model_dump_json() == e1r.model_dump_json()

    e2 = Event(rid=rid, event_type=EventType.UPDATE, manifest=m)
    e2r = Event.model_validate(e2.model_dump())
    assert e2 == e2r
    assert e2.model_dump_json() == e2r.model_dump_json()