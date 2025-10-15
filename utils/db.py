import json
import pyrebase

with open("firebase_config.json") as f:
    firebase_config = json.load(f)

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()  # For authentication if needed
db = firebase.database()  # Real-time database
