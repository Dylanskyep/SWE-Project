import streamlit as st


if "user_role" not in st.session_state or st.session_state.user_role != "volunteer":
    st.error("Unauthorized access. Please log in as a volunteer.")
    st.stop()

st.title("User Dashboard")
st.write(f"Welcome, {st.session_state.user_email}!")

if st.button("Logout"):
    st.session_state.clear()
    st.session_state.page = "welcome"
