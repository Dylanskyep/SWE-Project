from typing import List, Dict, Optional, Tuple
from datetime import datetime
#from google.cloud.firestore_v1.base_transaction import BaseTransaction
from google.cloud import firestore
from .firebase_config import get_db

def _events_col():
    return get_db.collection("events")

def _today_iso() -> str:
    return datetime.now().date().isoformat()

def create_event(event_data: Dict) -> str:
    event_data = dict(data)
    event_data.setdefault("title", "Untitled Event")
    event_data.setdefault("description", "")
    event_data.setdefault("date", _today_iso())
    event_data.setdefault("time", "00:00")
    event_data.setdefault("location", "")
    event_data.setdefault("capacity", 0)

    ref = _events_col().document()
    ref.set(data)
    return ref.id

def get_upcoming_events(limit: int = 100) -> List[Tuple[str, Dict]]:
    gb = get_db()
    try:
        q = _events_col().where("date", ">=", _today_iso()).order_by("date").order_by("time").limit(limit)
        docs = q.limit(limit).stream()
        results = [(d.id, d.to_dict() or {}) for d in docs]
        if results:
            return results
    except Exception:
        pass
    
def get_event(event_id: str) -> Optional[Dict]:
    snap = _events_col().document(event_id).get()
    if snap.exists:
        return snap.to_dict()
    else:
        return None
    
def update_event(event_id: str, data: Dict):
    _events_col().document(event_id).set(data, merge=True)

def delete_event(event_id: str):
    _events_col().document(event_id).delete()

def _read_volunteers_subcol(event_id: str) -> List[Dict]:
    regs = _events_col().document(event_id).collection("volunteers").stream()
    output = []
    