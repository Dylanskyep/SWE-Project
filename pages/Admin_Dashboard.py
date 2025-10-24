import streamlit as st
from services.event_service import list_admin_events

if "role" not in st.session_state or st.session_state.role != "admin":
    st.error("Unauthorized access. Please log in as an admin.")
    st.stop()
    
admin_id = st.session_state.get("userid", "")
admin_name = st.session_state.get("user_name", "")
admin_email = st.session_state.get("user_email", "")

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
    box-shadow: 0 4px 16px rgba(0,0,0,0.06); 
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
</style>
<div class="title">Admin Dashboard</div>
""", unsafe_allow_html=True)

st.write("")
st.subheader(f"Welcome, {admin_name or admin_email}!")
st.subheader("Your Events")

events = list_admin_events(admin_id)
if not events:
    st.info("You have not created any events yet.")
else:
    for ev in events:
        with st.container():
            st.markdown(f"""
        <div class="event-card">
            <h4>{ev.get('title', 'Untitled Event')}</h4>
            <p><b>Date:</b> {ev.get('date', 'TBD')} at {ev.get('time', '00:00')}</p>
            <p><b>Location:</b> {ev.get('location', 'TBD')}</p>
            <p><b>Description:</b> {ev.get('description', '')}</p>
            <p><b>Capacity:</b> {ev.get('capacity', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
st.write("")
col1, spacer, col2 = st.columns([2, 7, 1])
with col1:
    if st.button("Create New Event"):
        st.switch_page("pages/event_detail.py")
with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "welcome"
        st.rerun()