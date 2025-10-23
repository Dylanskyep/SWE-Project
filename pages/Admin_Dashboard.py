import streamlit as st

if "role" not in st.session_state or st.session_state.role != "admin":
    st.error("Unauthorized access. Please navigate back to the iVolunteer login page in using the top left navigation menu.")
    st.stop()
    
st.title("Admin Dashboard")
st.write(f"Welcome, {st.session_state.user_email}!")

if st.button("Logout"):
    st.session_state.clear()
    st.session_state.page = "welcome"
    st.rerun()