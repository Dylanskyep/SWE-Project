import hashlib
from utils.db import db

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Volunteer functions
def create_volunteer(name: str, email: str, password: str):
    users = db.child("volunteers").get().val() or {}
    if any(u['email'].lower() == email.lower() for u in users.values()):
        return False, "Email already registered"

    db.child("volunteers").push({
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": "volunteer"
    })
    return True, "Account created successfully"

def login_volunteer(email: str, password: str):
    users = db.child("volunteers").get().val() or {}
    for uid, user in users.items():
        if user['email'].lower() == email.lower() and user['password'] == hash_password(password):
            return True, {
                "user_id": uid,
                "name": user['name'],
                "email": user['email'],
                "role": "volunteer"
            }
    return False, "Invalid email or password"

# Admin functions
ADMIN_KEY = "admin123"  # For testing purposes

def create_admin(name: str, email: str, password: str):
    users = db.child("admins").get().val() or {}
    if any(u['email'].lower() == email.lower() for u in users.values()):
        return False, "Email already registered"

    db.child("admins").push({
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": "admin"
    })
    return True, "Admin account created successfully"

def login_admin(email: str, password: str, key: str):
    if key != ADMIN_KEY:
        return False, "Invalid admin key"

    users = db.child("admins").get().val() or {}
    for uid, user in users.items():
        if user['email'].lower() == email.lower() and user['password'] == hash_password(password):
            return True, {
                "user_id": uid,
                "name": user['name'],
                "email": user['email'],
                "role": "admin"
            }
    return False, "Invalid email or password"
