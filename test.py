from utils.auth import create_volunteer, login_volunteer, create_admin, login_admin

# --- Test data ---
volunteer_test = {
    "name": "Alice",
    "email": "alice@test.com",
    "password": "volpass123"
}

admin_test = {
    "name": "Bob",
    "email": "bob@test.com",
    "password": "adminpass123"
}

ADMIN_KEY = "admin123"

# --- Volunteer Tests ---
print("=== Volunteer Signup Test ===")
success, msg = create_volunteer(volunteer_test['name'], volunteer_test['email'], volunteer_test['password'])
print("Signup:", msg)

print("\n=== Volunteer Login Test ===")
success, info = login_volunteer(volunteer_test['email'], volunteer_test['password'])
if success:
    print("Login success:", info)
else:
    print("Login failed:", info)

# --- Admin Tests ---
print("\n=== Admin Signup Test ===")
success, msg = create_admin(admin_test['name'], admin_test['email'], admin_test['password'])
print("Admin signup:", msg)

print("\n=== Admin Login Test ===")
success, info = login_admin(admin_test['email'], admin_test['password'], ADMIN_KEY)
if success:
    print("Admin login success:", info)
else:
    print("Admin login failed:", info)

print("\n=== Admin Login Fail Test (wrong key) ===")
success, info = login_admin(admin_test['email'], admin_test['password'], "wrongkey")
if success:
    print("Admin login successful (should not happen!)", info)
else:
    print("Admin login failed as expected:", info)


# Create an 'events' node with a placeholder child
db.child("events").push({
    "dummy": True
})

print("Events node created!")
