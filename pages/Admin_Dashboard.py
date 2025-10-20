import streamlit as st

if "user_role" not in st.session_state or st.session_state.user_role != "admin":
    st.error("Unauthorized access. Please log in as an admin.")
    st.stop()
    
st.title("Admin Dashboard")
st.write(f"Welcome, {st.session_state.user_email}!")

if st.button("Logout"):
    st.session_state.clear()
    st.session_state.page = "welcome"