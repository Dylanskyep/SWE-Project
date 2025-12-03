import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_config.json")
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_collection(name):
  return db.collection(name)