from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, firestore
from functools import lru_cache

load_dotenv()

@lru_cache
def get_db():
    """Initialize and return Firestore client."""
    
    creds_path = os.getenv("FIREBASE_CREDS")
    if not creds_path or not os.path.exists(creds_path):
        raise RuntimeError("FIREBASE_CREDS not set or invalid.")

    if not firebase_admin._apps:
        cred = credentials.Certificate(creds_path)
        firebase_admin.initialize_app(cred)

    return firestore.client()