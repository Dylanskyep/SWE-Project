import hashlib
from utils.db import db

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

ADMIN_KEY = "admin123"  # replace later or move to env variable

def create_user(name: str, email: str, password: str, role: str, admin_key: str = None):
    users_ref = db.collection("users")
    existing = users_ref.where("email", "==", email.lower()).stream()
    if any(existing):
        return False, "Email already registered"
    if role == "admin":
        if admin_key != ADMIN_KEY:
            return False, "Invalid admin key"
    users_ref.add({
        "name": name,
        "email": email.lower(),
        "password": hash_password(password),
        "role": role
    })
    return True, "User created successfully"

def login_user(email: str, password: str):
    users_ref = db.collection("users")
    docs = users_ref.where("email", "==", email.lower()).stream()
    for doc in docs:
        user = doc.to_dict()
        if user["password"] == hash_password(password):
            return True, {
                "user_id": doc.id,
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
    return False, "Invalid email or password"

def create_volunteer(name, email, password):
    return create_user(name, email, password, role="volunteer")

def create_admin(name, email, password, admin_key):
    return create_user(name, email, password, role="admin", admin_key=admin_key)
