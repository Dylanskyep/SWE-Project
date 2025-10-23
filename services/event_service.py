from typing import List, Dict, Optional, Tuple
from datetime import datetime
from google.cloud import firestore
from services.firebase_config import get_db
from datetime import datetime


def _events_col():
    return get_db().collection("events")

def _today_iso() -> str:
    return datetime.now().date().isoformat()

"""Events CRUD Operations"""

def create_event(data: dict):
    #required fields
    events_ref = _events_col()
    new_event = {
        "title": data.get("title", "Untitled Event"),
        "description": data.get("description", ""),
        "date": data.get("date", ""),
        "time": data.get("time", "00:00"),
        "location": data.get("location", "TBD"),
        "capacity": int(data.get("capacity", 0)),
    }

    ref = events_ref.document()
    ref.set(new_event)
    return ref.id

def get_upcoming_events():
    #showing events with date today or later, sorted by date then time
    now = datetime.now().strftime("%Y-%m-%d")

    query = (_events_col()
             .where("date", ">=", now)
             .order_by("date")
             .order_by("time"))

    snaps = query.stream()
    return [(s.id, s.to_dict() or {}) for s in snaps]
    
def get_event(event_id):
    if not event_id:
        return None
    
    try:
        db = get_db()
        doc_ref = db.collection("events").document(event_id)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            print(f"[DEBUG] Event with ID {event_id} not found in Firestore.")
            return None
    except Exception as e:
        print(f"[ERROR] An error occurred while fetching event: {e}")
        return None

    
def update_event(event_id, data):
    event_ref = _events_col().document(event_id)
    event_ref.set(data, merge=True)

def delete_event(event_id: str):
    _events_col().document(event_id).delete()

"""Registrations"""

def list_registrations(event_id: str) -> List[Dict]:
    regs = (
        _events_col()
        .document(event_id)
        .collection("registrations")
        .stream()
    )
    return [r.to_dict() or {} for r in regs]

@firestore.transactional
def register_user(event_id: str, user_id:str, name:str, email:str) -> None:
    """Register a user and decrement capacity"""
    db = get_db()
    tx = db.transaction()
    _register_tx(tx, event_id, user_id, name, email)

def _register_tx(tx, event_id: str, user_id:str, name:str, email:str):
    event_ref = _events_col().document(event_id)
    event_snap = event_ref.get(transaction=tx)
    if not event_snap.exists:
        raise ValueError("Event does not exist.")
    event_data = event_snap.to_dict() or {}
    capacity = int(event_data.get("capacity", 0))
    if capacity <= 0:
        raise ValueError("Event is full.")
    
    reg_ref = event_ref.collection("registrations").document(user_id)
    reg_snap = reg_ref.get(transaction=tx)
    if reg_snap.exists:
        return    
    # Add registration
    reg_data = {
        "user_id": user_id,
        "name": name,
        "email": email,
    }
    tx.set(reg_ref, reg_data)
    
    # Decrement capacity
    tx.update(event_ref, {"capacity": capacity - 1})