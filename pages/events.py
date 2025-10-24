import streamlit as st
from services.event_service import get_upcoming_events, register_user
st.set_page_config(layout="wide")

if "role" not in st.session_state or st.session_state.role != "volunteer":
    st.error("Unauthorized access. Please log in as a volunteer.")
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
.event-card {
    background-color: rgba(255,255,255,0.85);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}
.event-card h4 {
    color: rgb(95,105,96);
    margin-bottom: 5px;
}
.event-card p {
    margin: 0 0 8px 0;
}
.stButton>button {
    background-color: rgb(95,105,96);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    padding: 0.4em 1em;
    transition: all 0.2s ease;
}
.stButton>button:hover {
    background-color: rgb(75,82,76);
}
</style>

<div class="title">Volunteer Events</div>
""", unsafe_allow_html=True)

st.write("")
st.subheader(f"Welcome, {user_name or user_email}! Here are the upcoming volunteer opportunities:")
events = get_upcoming_events()

if not events:
    st.info("No upcoming events at the moment. Please check back later!")
else:
    for event_id, ev in events:
        st.markdown(f"""
        <div class="event-card">
            <h4>{ev.get('title', 'Untitled Event')}</h4>
            <p><b>Date:</b> {ev.get('date', 'TBD')} at {ev.get('time', '00:00')}</p>
            <p><b>Location:</b> {ev.get('location', 'TBD')}</p>
            <p><b>Description:</b> {ev.get('description', '')}</p>
            <p><b>Capacity:</b> {ev.get('capacity', '—')}</p>
        </div>
        """, unsafe_allow_html=True)

        if ev.get("capacity", 0) > 0:
            if st.button(f"Sign Up for {ev['title']}", key=f"signup_{event_id}"):
                try:
                    register_user(event_id, user_id, user_name, user_email)
                    st.success(f"You have registered for **{ev['title']}**!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error registering: {e}")
        else:
            st.warning("Event is full.")

st.write("---")

if st.button("Back to Dashboard"):
    st.switch_page("pages/User_Dashboard.py")