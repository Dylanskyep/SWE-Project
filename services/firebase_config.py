import os
import firebase_admin
from firebase_admin import credentials, firestore
from functools import lru_cache
@lru_cache(maxsize=1)

def get_db():
    """Initialize and return Firestore client."""
    
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDS")
        if not cred_path or not os.path.isfile(cred_path):
            raise RuntimeError("FIREBASE_CREDS not set or invalid.")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            "projectID": os.getenv("FIREBASE_PROJECT_ID")
        })
    return firestore.client()