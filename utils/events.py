from datetime import datetime
import pytz
from typing import Any, Dict, Optional
from utils.db import db

def now_eastern() -> str:
      eastern = pytz.timezone("America/New_York")
      return datetime.now(eastern).isoformat()

def create_event(title: str, description: str, date_str: str, time_str: str,
                 location: str, capacity: int, created_by: str, image_url: Optional[str] = None) -> tuple[bool, str]:
        if not title or not date_str or not time_str or not location:
            return False, "Title, date, time, and location are required"
        
        try:
              cap = int(capacity)
        except (TypeError, ValueError):
              return False, "Capacity must be a number"
        
        doc: Dict[str, Any] = {
            "title": title,
            "description": description,
            "date": date_str,
            "time": time_str,
            "location": location,
            "capacity": cap,
            "created_by": created_by,
            "image_url": image_url,
            "created_at": now_eastern(),
            "attendees": []
        }
        ref = db.collection("events").document()
        ref.set(doc)
        return True, ref.id

def list_events(order_by_date: bool = True, then_time: bool = True):
    col = db.collection("events")
    q = col
    if order_by_date:
        try:
            q = q.order_by("date")
        except Exception:
            pass
    out: list[Dict[str, Any]] = []
    for doc in q.stream():
        ev = doc.to_dict()
        ev["id"] = doc.id
        out.append(ev)
    return out

def get_event(event_id: str):
    snap = db.collection("events").document(event_id).get()
    if not snap.exists:
        return None
    ev = snap.to_dict()
    ev["id"] = snap.id
    return ev

def delete_event(event_id: str):
    db.collection("events").document(event_id).delete()
    return True