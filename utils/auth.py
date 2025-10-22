import hashlib
import re
from utils.db import db

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email.strip()))

ADMIN_KEY = "admin123"  # replace later or move to env variable

def create_user(name: str, email: str, password: str, role: str, admin_key: str = None):
    email = email.strip().lower()
    if not valid_email(email):
        return False, "Invalid email format"
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

def login_user(email: str, password: str, role: str = None):
    """
    Return user dict on successful login or None on failure
    If role is provided, require the user to have that role.
    This keeps the front-end 'if user:' checks working unchanged.
    """
    users_ref = db.collection("users")
    query = users_ref.where("email", "==", email.lower())
    if role:
        query = query.where("role", "==", role)

    docs = list(query.stream())
    if not docs:
        return None

    for doc in docs:
        user = doc.to_dict()
        if user.get("password") == hash_password(password):
            return {
                "user_id": doc.id,
                "name": user.get("name"),
                "email": user.get("email"),
                "role": user.get("role")
            }

    # Password didn't match any found account
    return None

def create_volunteer(name, email, password):
    return create_user(name, email, password, role="volunteer")

def create_admin(name, email, password, admin_key):
    return create_user(name, email, password, role="admin", admin_key=admin_key)
