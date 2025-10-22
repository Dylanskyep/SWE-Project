import streamlit as st


if "role" not in st.session_state or st.session_state.role != "volunteer":
    st.error("Unauthorized access. Please log in as a volunteer.")
    st.stop()

st.title("User Dashboard")
st.write(f"Welcome, {st.session_state.user_email}!")

if st.button("Logout"):
    st.session_state.clear()
    st.session_state.page = "welcome"
