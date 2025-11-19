import streamlit as st
from services.event_service import list_user_registrations, unregister_user
st.set_page_config(layout="wide")

if "role" not in st.session_state or st.session_state.role != "volunteer":
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

user_id = st.session_state.get("userid", "")
user_name = st.session_state.get("user_name", "")
user_email = st.session_state.get("user_email", "")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: rgb(244, 247, 246);
    color: rgb(138, 156, 140);
    font-family: "Helvetica", sans-serif;
}
.title {
    font-size: 50px;
    color: rgb(95, 105, 96) !important;
    font-weight: 600;
    text-align: left;
    line-height: 1.2;
    margin: 10px 0 2px 0;
    width: auto;
    border-right: none;
    white-space: normal;
}
.section {
    background-color: rgba(255,255,255,0.7);
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.event-card {
    background-color: rgba(255,255,255,0.95);
    border: 1px solid rgba(0,0,0,0.04);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 16px 0;                 
    box-shadow: 0 4px 16px rgba(0,0,0,0.3); 
}
.event-card h4 {
    color: rgb(95,105,96);
    margin: 0 0 6px 0;
}
.event-card p {
    margin: 0 0 8px 0;
}
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
.event-wrapper {
    max-width: 920px;
    margin: 12px auto;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 12px;
    padding: 12px;
    background: rgba(255,255,255,0.98);
}
.event-wrapper .event-card {
    margin: 0;
}
</style>
<div class="title">Volunteer Dashboard</div>
""", unsafe_allow_html=True)


st.write("")
st.subheader(f"Welcome, {user_name or user_email}!")
st.subheader("My Upcoming Events")

events = list_user_registrations(user_id)
 
if not events:
    st.info("You haven’t signed up for any events yet.")
else:
    for ev in events:
        event_id = ev.get("event_id")
        st.markdown('<div class="event-wrapper">', unsafe_allow_html=True)
        cols = st.columns([9, 1])
        with cols[0]:
            st.markdown(f"""
            <div class="event-card">
                <h4>{ev.get('title', 'Untitled Event')}</h4>
                <p><b>Date:</b> {ev.get('date', 'TBD')} at {ev.get('time', '00:00')}</p>
                <p><b>Location:</b> {ev.get('location', 'TBD')}</p>
                <p><b>Description:</b> {ev.get('description', '')}</p>
            </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            st.write("")
            if event_id:
                if st.button("Unregister", key=f"unreg_{event_id}"):
                    try:
                        unregister_user(event_id, user_id)
                        st.success(f"You have been unregistered from **{ev.get('title','this event')}**.")
                        st.rerun()
                    except ValueError as e:
                        st.warning(str(e))
                    except Exception as e:
                        st.error(f"Error unregistering: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

st.write("")
col1, spacer, col2 = st.columns([2, 7, 1])
with col1:
    if st.button("Browse Events"):
        st.switch_page("pages/events.py")
with col2:
    if st.button("Logout"):
        st.session_state.clear()
        try:
            st.query_params()
        except Exception:
            pass
        try:
            st.switch_page("iVolunteer.py")
        except Exception:
            st.session_state.page = "welcome"
            st.rerun()