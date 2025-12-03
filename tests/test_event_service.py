def test_sanity():
    assert 1 == 1
# test event_service.py
import types
from services import event_service

class FakeDoc:
    def __init__(self, data, doc_id="fake-id"):
        self._data = data
        self.id = doc_id

    def to_dict(self):
        return self._data

class FakeCollection:
    def __init__(self):
        self._docs = {}
        self._counter = 0

    def document(self, doc_id=None):
        if doc_id is None:
            doc_id = f"doc-{self._counter}"
            self._counter += 1

        # create a light wrapper with set / get / delete
        col = self

        class DocRef:
            def __init__(self, _id):
                self.id = _id

            def set(self, data, **kwargs):
                # Simulate Firestore's set(..., merge=True/False)
                merge = kwargs.get("merge", False)
                existing = col._docs.get(self.id, {})
                if merge and isinstance(existing, dict):
                    # merge fields into existing
                    existing.update(data)
                    col._docs[self.id] = existing
                else:
                    # overwrite
                    col._docs[self.id] = data

            def get(self):
                if self.id in col._docs:
                    return FakeDoc(col._docs[self.id], self.id)
                return FakeDoc(None, self.id)

            def delete(self):
                col._docs.pop(self.id, None)

        return DocRef(doc_id)

    def stream(self):
        for doc_id, data in self._docs.items():
            yield FakeDoc(data, doc_id)

# ---- helper to monkeypatch events collection ----

def fake_events_col():
    if not hasattr(fake_events_col, "_col"):
        fake_events_col._col = FakeCollection()
    return fake_events_col._col

def setup_module(module):
    # monkeypatch the internal _events_col function
    event_service._events_col = fake_events_col

def teardown_module(module):
    # reset between test runs if needed
    if hasattr(fake_events_col, "_col"):
        del fake_events_col._col

def test_create_event_stores_expected_fields():
    data = {
        "title": "Test Event",
        "description": "Testing",
        "date": "2025-11-01",
        "time": "10:00",
        "location": "UF Campus",
        "capacity": 20,
    }

    event_id = event_service.create_event(data)
    col = fake_events_col()
    stored_doc = col.document(event_id).get().to_dict()

    assert stored_doc["title"] == data["title"]
    assert stored_doc["description"] == data["description"]
    assert stored_doc["date"] == data["date"]
    assert stored_doc["time"] == data["time"]
    assert stored_doc["location"] == data["location"]
    assert stored_doc["capacity"] == data["capacity"]

def test_update_event_changes_fields():
    # create first
    event_id = event_service.create_event({
        "title": "Original Title",
        "description": "Old desc",
        "date": "2025-11-01",
        "time": "10:00",
        "location": "UF",
        "capacity": 10,
    })

    # update
    event_service.update_event(event_id, {
        "title": "New Title",
        "description": "New desc",
        "capacity": 15,
    })

    col = fake_events_col()
    stored_doc = col.document(event_id).get().to_dict()
    assert stored_doc["title"] == "New Title"
    assert stored_doc["description"] == "New desc"
    assert stored_doc["capacity"] == 15

def test_delete_event_removes_document():
    event_id = event_service.create_event({
        "title": "Delete Me",
        "description": "temp",
        "date": "2025-11-01",
        "time": "10:00",
        "location": "UF",
        "capacity": 5,
    })

    col = fake_events_col()
    # sanity check
    assert col.document(event_id).get().to_dict() is not None

    event_service.delete_event(event_id)

    assert col.document(event_id).get().to_dict() is None

