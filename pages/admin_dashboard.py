import streamlit as st
from services.event_service import (
    get_upcoming_events, get_event, create_event, update_event, delete_event, list_registrations
)
from datetime import datetime, date, time

st.set_page_config(page_title="Admin Dashboard", page_icon="🛠️")
st.title("Admin - Events")

st.info("Hook actual admin auth later; this page assumes you are an admin.")

"""Create Event"""
with st.form("event_form", clear_on_submit=True):
    title = st.text_input("Event Title")
    description = st.text_area("Description")
    date_ = st.date_input("Date", value=None)
    time_ = st.time_input("Time", value=None)
    location = st.text_input("Location")
    capacity = st.number_input("Capacity", min_value=1, step=1)
    submitted = st.form_submit_button("Create Event")

    if submitted:
        # validate all fields
        errors = []
        if not title.strip():
            errors.append("Title is required.")
        if not description.strip():
            errors.append("Description is required.")
        if date_ is None:
            errors.append("Please select a date.")
        if time_ is None:
            errors.append("Please select a time.")
        if not location.strip():
            errors.append("Location is required.")
        if capacity < 1:
            errors.append("Capacity must be at least 1.")

        if errors:
            st.error("⚠️ Please fix the following issues:\n- " + "\n- ".join(errors))
        else:
            # convert to Firestore strings
            formatted_date = date_.strftime("%Y-%m-%d")
            formatted_time = time_.strftime("%H:%M")

            eid = create_event({
                "title": title,
                "description": description,
                "date": formatted_date,
                "time": formatted_time,
                "location": location,
                "capacity": int(capacity),
            })
            st.success(f"Event '{title}' created successfully!")


st.write("---")

"""Manage Existing Events"""

events = get_upcoming_events()

if "last_action" in st.session_state:
    del st.session_state["last_action"]

if not events:
    st.caption("No upcoming events.")
else:
    for event_id, event in events:
        with st.container(border=True):
            st.subheader(event.get("title", "Untitled"))
            st.caption(f"{event.get('date', 'TBD')} • {event.get('time', '')} • {event.get('location', 'TBD')}")
            st.write(event.get("description", ""))
            st.write(f"Capacity: **{int(event.get('capacity', 0))}**")

            with st.expander("Roster"):
                regs = list_registrations(event_id)
                if not regs:
                    st.caption("No registrations yet.")
                else:
                    for reg in regs:
                        st.write(f"- {reg.get('name', 'Unknown')} - {reg.get('email', 'No Email')}")

            with st.expander("Edit / Delete Event"):
                with st.form(f"edit_{event_id}", clear_on_submit=False):
                    new_title = st.text_input("Title", value=event.get("title", ""))
                    new_description = st.text_area("Description", value=event.get("description", ""))
                    new_date_str = event.get("date", "")
                    new_time_str = event.get("time", "")

                    new_date = st.date_input("Date", value=datetime.strptime(new_date_str, "%Y-%m-%d").date() if new_date_str else date.today())
                    new_time = st.time_input("Time", value=datetime.strptime(new_time_str, "%H:%M").time() if new_time_str else time(0, 0))
                    
                    new_location = st.text_input("Location", value=event.get("location", ""))
                    new_capacity = st.number_input("Capacity", min_value=1, step=1, value=int(event.get("capacity", 1)))

                    # title = st.text_input("Title", value=event.get("title", ""))
                    # description = st.text_area("Description", value=event.get("description", ""))
                    # col1, col2 = st.columns(2)
                    # with col1:
                    #     date = st.text_input("Date (YYYY-MM-DD)", value=event.get("date", ""))
                    #     location = st.text_input("Location", value=event.get("location", ""))
                    # with col2:
                    #     time = st.text_input("Time (HH:MM)", value=event.get("time", ""))
                    #     capacity = st.number_input("Capacity", min_value=0, step=1, value=int(event.get("capacity", 0)))
                    colA, colB = st.columns(2)
                    with colA:
                        updated = st.form_submit_button("Update Event")
                    with colB:
                        deleted = st.form_submit_button("Delete Event", type="secondary")

                if updated:
                    if not all([new_title.strip(), new_description.strip(), new_date, new_time, new_location.strip(), new_capacity]):
                        st.error("Please fill in all fields before saving.")
                    else:
                        formattedNew_date = new_date.strftime("%Y-%m-%d")
                        formattedNew_time = new_time.strftime("%H:%M")

                        update_event(event_id, {
                            "title": new_title,
                            "description": new_description,
                            "date": formattedNew_date,
                            "time": formattedNew_time,
                            "location": new_location,
                            "capacity": int(new_capacity)
                        })
                        st.success("Event updated successfully!")
                        st.session_state["last_action"] = "event_updated"
                        st.rerun()  # reloads the page cleanly
                if deleted:
                    delete_event(event_id)
                    st.success("Event deleted successfully.")
