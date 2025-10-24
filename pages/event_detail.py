import streamlit as st
from services.event_service import get_event, register_user, list_registrations

st.set_page_config(page_title="Event Detail", page_icon="📋")

st.write("🔍 DEBUG PARAMS:", st.query_params)


if st.button("⬅ Back to Events"):
    st.switch_page("pages/events.py")

query_params = st.query_params
event_id = query_params.get("eid")

st.caption(f"🔍 DEBUG: Loaded event_id = {event_id}")


# if not event_id:
#     st.warning("No event ID provided. Please go back to the Events page and choose 'View Details'.")
#     st.stop()

event = get_event(event_id)
if not event:
    st.error("Event not found.")
    st.stop()

st.title(event.get("title", "Untitled Event"))
st.write(f"📅 **Date:** {event.get('date', 'N/A')}")
st.write(f"🕒 **Time:** {event.get('time', 'N/A')}")
st.write(f"📍 **Location:** {event.get('location', 'N/A')}")
st.write(f"👥 **Capacity:** {event.get('capacity', 'N/A')}")
st.write("---")
st.write(f"📝 **Description:**\n\n{event.get('description', 'No description provided.')}")
event
remaining_spots = int(event.get("capacity", 0))
st.write(f"**Spots remaining:**{remaining_spots}")

with st.expander("Attendees"):
    registrations = list_registrations(event_id)
    if not registrations:
        st.caption("No registrations yet.")
    else:
        for reg in registrations:
            st.write(f"- {reg.get('name', 'Unknown')}")

st.write("---")
st.subheader("Register for this Event")

name = st.text_input("Full Name")
email = st.text_input("Email Address")
uid = (name.lower().replace(" ", "_") if name else "").strip()

register_disabled = not name or not email or remaining_spots <= 0

if st.button("Register", disabled=register_disabled):
    try:
        register_user(event_id, uid or email, name, email)
        st.success("Successfully registered!")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Registration failed: {str(e)}")