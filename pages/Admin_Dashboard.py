import streamlit as st
from datetime import datetime, date, time
from services.event_service import (
    get_upcoming_events,
    create_event,
    update_event,
    delete_event,
    list_registrations,
)

if "role" not in st.session_state or st.session_state.role != "admin":
    st.error("Unauthorized access. Please log in as an admin.")
    try:
        st.query_params()
    except Exception:
        pass
    try:
        st.switch_page("iVolunteer.py")
    except Exception:
        st.session_state.page = "welcome"
        st.rerun()
    st.stop()

admin_name = st.session_state.get("user_name", "")
admin_email = st.session_state.get("user_email", "")

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
/* overall page background + font + top spacing */
[data-testid="stAppViewContainer"] {
    background-color: rgb(244, 247, 246);
    color: rgb(138, 156, 140);
    font-family: "Helvetica", sans-serif;
    padding-top: 20px !important;
}

/* remove thick white HR-style dividers */
hr, [data-testid="stDivider"], .stMarkdown hr {
    display: none !important;
}

/* page title */
.title {
    font-size: 50px;
    color: rgb(95, 105, 96) !important;
    font-weight: 600;
    text-align: left;
    line-height: 1.2;
    margin: 0 0 10px 0;
}

/* welcome subtext under title */
.welcome-line {
    font-size: 16px;
    color: rgb(95,105,96);
    margin-bottom: 0.5rem;
}

/* header row subtle divider */
.header-divider {
    border-bottom: 1px solid rgba(95,105,96,0.15);
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}

/* section headers */
.section-header {
    font-size: 24px;
    color: rgb(95,105,96);
    font-weight: 600;
    margin-bottom: 0.5rem;
}

/* outer section container (card around each block) */
.section {
    background-color: rgba(255,255,255,0.7);
    border-radius: 15px;
    padding: 24px;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

/* per-event card */
.event-card {
    background-color: rgba(255,255,255,0.95);
    border: 1px solid rgba(0,0,0,0.04);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 16px 0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.event-card h4 {
    color: rgb(95,105,96);
    margin: 0 0 6px 0;
}
.event-card p {
    margin: 0 0 8px 0;
    color: rgb(75,82,76);
}

/* roster lines */
.roster-line {
    color: rgb(75,82,76);
    font-size: 15px;
    margin-bottom: 4px;
}

/* main buttons (Create Event, Update Event, etc.) */
.stButton > button {
    background-color: rgb(95,105,96);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    padding: 0.45em 1.1em;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background-color: rgb(75,82,76);
}

/* "secondary" style button for Delete */
div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: rgba(95,105,96,0.1) !important;
    color: rgb(95,105,96) !important;
    border: 1px solid rgb(95,105,96) !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background-color: rgba(75,82,76,0.15) !important;
    color: rgb(75,82,76) !important;
    border-color: rgb(75,82,76) !important;
}
</style>
""", unsafe_allow_html=True)
header_left, header_right = st.columns([6, 1])

with header_left:
    st.markdown('<div class="title">Admin Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="welcome-line">Welcome, {admin_name or admin_email}!</div>',
        unsafe_allow_html=True
    )

with header_right:
    if st.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "welcome"
        st.rerun()
        try:
            st.query_params()
        except Exception:
            pass
        try:
            st.switch_page("iVolunteer.py")
        except Exception:
            st.session_state.page = "welcome"
            st.rerun()

st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">Create New Event</div>', unsafe_allow_html=True)

# Helper functions for time parsing/formatting
def parse_stored_time_to_timeobj(stored_time: str):
    """
    Accepts a stored time string that may be:
      - "HH:MM" (24-hour)
      - "H:MM AM/PM" or "HH:MM AM/PM"
    Returns a datetime.time object, or None on failure.
    """
    if not stored_time:
        return None
    s = stored_time.strip().replace(".", "")
    try:
        # Try AM/PM first
        if "AM" in s.upper() or "PM" in s.upper():
            return datetime.strptime(s.upper(), "%I:%M %p").time()
        # Fall back to 24-hour
        return datetime.strptime(s, "%H:%M").time()
    except Exception:
        return None

def format_time_for_display(stored_time: str):
    """
    Returns a time string in "HH:MM AM/PM" for display.
    Accepts stored_time in either "%H:%M" or "%I:%M %p".
    If parsing fails, returns the original string.
    """
    if not stored_time:
        return ""
    s = stored_time.strip().replace(".", "")
    try:
        if "AM" in s.upper() or "PM" in s.upper():
            # Already in AM/PM — normalize spacing and case
            return datetime.strptime(s.upper(), "%I:%M %p").strftime("%I:%M %p")
        # Try parsing as 24-hour and convert
        return datetime.strptime(s, "%H:%M").strftime("%I:%M %p")
    except Exception:
        return stored_time

with st.form("event_form", clear_on_submit=True):
    title = st.text_input("Event Title")
    description = st.text_area("Description")
    date_ = st.date_input("Date", value=None)
    time_ = st.time_input("Time", value=None)
    location = st.text_input("Location")
    capacity = st.number_input("Capacity", min_value=1, step=1)

    submitted = st.form_submit_button("Create Event")

    if submitted:
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
            st.error("Please fix the following issues:\n- " + "\n- ".join(errors))
        else:
            formatted_date = date_.strftime("%Y-%m-%d")
            # Save time in 12-hour AM/PM string format for user-friendly display
            formatted_time = time_.strftime("%I:%M %p")

            create_event({
                "title": title,
                "description": description,
                "date": formatted_date,
                "time": formatted_time,
                "location": location,
                "capacity": int(capacity),
            })
            st.success(f"Event '{title}' created successfully!")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">Manage Your Events</div>', unsafe_allow_html=True)

events = get_upcoming_events()

if not events:
    st.caption("No upcoming events.")
else:
    for event_id, event in events:
        # Display time in 12-hour AM/PM format (convert if stored as 24-hour)
        stored_display_time = format_time_for_display(event.get("time", ""))
        st.markdown(f"""
        <div class="event-card">
            <h4>{event.get('title', 'Untitled')}</h4>
            <p><b>Date:</b> {event.get('date', 'TBD')} at {stored_display_time}</p>
            <p><b>Location:</b> {event.get('location', 'TBD')}</p>
            <p><b>Description:</b> {event.get('description', '')}</p>
            <p><b>Capacity:</b> {int(event.get('capacity', 0))}</p>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("View Registrations"):
            regs = list_registrations(event_id)
            if not regs:
                st.caption("No registrations yet.")
            else:
                for reg in regs:
                    st.markdown(
                        f"<div class='roster-line'>• {reg.get('name','Unknown')} — {reg.get('email','(no email)')}</div>",
                        unsafe_allow_html=True
                    )

        with st.expander("Edit / Delete Event"):
            with st.form(f"edit_{event_id}", clear_on_submit=False):
                new_title = st.text_input("Title", value=event.get("title", ""))
                new_description = st.text_area("Description", value=event.get("description", ""))
                stored_date = event.get("date", "")
                try:
                    default_date = datetime.strptime(stored_date, "%Y-%m-%d").date() if stored_date else date.today()
                except Exception:
                    default_date = date.today()
                stored_time = event.get("time", "")
                try:
                    # Use helper to handle multiple stored formats
                    parsed = parse_stored_time_to_timeobj(stored_time)
                    default_time = parsed if parsed is not None else time(0, 0)
                except Exception:
                    default_time = time(0, 0)

                new_date = st.date_input("Date", value=default_date)
                new_time = st.time_input("Time", value=default_time)

                new_location = st.text_input("Location", value=event.get("location", ""))
                new_capacity = st.number_input(
                    "Capacity",
                    min_value=1,
                    step=1,
                    value=int(event.get("capacity", 1))
                )
                colA, colB = st.columns(2)
                with colA:
                    updated = st.form_submit_button("Update Event")
                with colB:
                    deleted = st.form_submit_button("Delete Event", type="secondary")
            if updated:
                if not all([
                    new_title.strip(),
                    new_description.strip(),
                    new_date,
                    new_time,
                    new_location.strip(),
                    new_capacity,
                ]):
                    st.error("Please fill in all fields before saving.")
                else:
                    formatted_date = new_date.strftime("%Y-%m-%d")
                    # Save updates in 12-hour AM/PM form
                    formatted_time = new_time.strftime("%I:%M %p")

                    update_event(
                        event_id,
                        {
                            "title": new_title,
                            "description": new_description,
                            "date": formatted_date,
                            "time": formatted_time,
                            "location": new_location,
                            "capacity": int(new_capacity),
                        },
                    )
                    st.success("Event updated successfully!")
                    st.rerun()
            if deleted:
                delete_event(event_id)
                st.success("Event deleted successfully.")
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
