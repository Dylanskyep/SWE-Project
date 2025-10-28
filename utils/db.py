import firebase_admin
from firebase_admin import credentials, firestore

<<<<<<< HEAD
cred = credentials.Certificate("firebase_config.json")  # replace with your new private key JSON

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# firebase_admin.initialize_app(cred)
=======
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
>>>>>>> a5633e015d36689f2ba5803e19457ea6bf0c1c0a

db = firestore.client()

# def get_collection(name):
#     return db.collection(name)