import streamlit as st
from datetime import datetime
import pytz
import hashlib
from typing import Dict, Any
from utils.db import db

def now()-> str:
      eastern = pytz.timezone("America/New_York")
      return datetime.now(eastern).isoformat()

def create_event(title: str, description: str, date_str: str, time_str: str,
                 location: str, capacity: int, created_by: str, image_url: str | None = None):
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
            "created_at": now(),
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
        e = doc.to_dict()
        e["id"] = doc.id
        out.append(e)
    return out

def get_event(event_id: str):
    snap = db.collection("events").document(event_id).get()
    if not snap.exists:
        return None
    e = snap.to_dict()
    e["id"] = snap.id
    return e

def delete_event(event_id: str):
    db.collection("events").document(event_id).delete()
    return True