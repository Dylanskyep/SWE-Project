from utils.auth import create_volunteer, create_admin, login_user
from services.event_service import (
    create_event, register_user, get_event, list_user_registrations, delete_event
)
from utils.db import db

print("Running tests...\n")

# volunteer test data
vol = {
    "name": "Alice TestUser",
    "email": "alice_testuser@example.com",
    "password": "volpass123"
}

# admin test data
admin = {
    "name": "Bob TestAdmin",
    "email": "bob_testadmin@example.com",
    "password": "adminpass123"
}
ADMIN_KEY = "admin123"

# Volunteer signup
success, msg = create_volunteer(vol["name"], vol["email"], vol["password"])
assert success, "Volunteer should be able to sign up"
assert msg == "User created successfully"

# Duplicate signup, fails
success, msg = create_volunteer(vol["name"], vol["email"], vol["password"])
assert not success, "Duplicate volunteer signup should not work"
assert msg == "Email already registered"

# Volunteer login
user = login_user(vol["email"], vol["password"], role="volunteer")
assert user is not None, "Volunteer login should succeed with correct password"
assert user["email"] == vol["email"]

# Wrong password, fails
wrong = login_user(vol["email"], "wrongpass", role="volunteer")
assert wrong is None, "Volunteer login should fail with wrong password"

# Admin signup
success, msg = create_admin(admin["name"], admin["email"], admin["password"], ADMIN_KEY)
assert success, "Admin signup should work"

# Admin login
admin_user = login_user(admin["email"], admin["password"], role="admin")
assert admin_user is not None, "Admin login should succeed"
assert admin_user["email"] == admin["email"]

# Wrong admin password, fails
wrong_admin = login_user(admin["email"], "wrongpass", role="admin")
assert wrong_admin is None, "Admin login should fail with bad password"

# Create an event to test with
event_id = create_event({
    "title": "Beach Cleanup",
    "description": "Join us for a community cleanup!",
    "date": "2025-12-25",
    "time": "09:00",
    "location": "Main Beach",
    "capacity": 3
})
assert event_id, "Event should be created successfully"

# Register the first user
register_user(event_id, "user1", "Alice", vol["email"])
event = get_event(event_id)
assert event["capacity"] == 2, "Capacity should drop to 2 after one signup"

# Registering the same user again should not work
try:
    register_user(event_id, "user1", "Alice", vol["email"])
    raise AssertionError("Duplicate registration should not be allowed")
except Exception:
    pass

# Fill up the event
register_user(event_id, "user2", "Charlie", "charlie@example.com")
register_user(event_id, "user3", "Dana", "dana@example.com")
event = get_event(event_id)
assert event["capacity"] == 0, "Event should now be full"

# Try signing up after full
try:
    register_user(event_id, "user4", "Eve", "eve@example.com")
    raise AssertionError("Should not be able to register when event is full")
except Exception:
    pass

# Check that user1 shows this event in their list
user_events = list_user_registrations("user1")
assert len(user_events) >= 1, "User1 should have a registered event"
assert user_events[0]["title"] == "Beach Cleanup"


# Clean up test data
print("\nCleaning up test data...")
for email in [vol["email"], admin["email"]]:
    docs = db.collection("users").where("email", "==", email).stream()
    for doc in docs:
        doc.reference.delete()
        print(f"Deleted user: {email}")
delete_event(event_id)
print("Deleted test event.")
print("\nAll tests completed successfully!\n")