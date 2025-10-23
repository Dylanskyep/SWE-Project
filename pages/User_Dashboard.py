import streamlit as st


if "role" not in st.session_state or st.session_state.role != "volunteer":
    st.error("Unauthorized access. Please navigate back to the iVolunteer login page in using the top left navigation menu.")
    st.stop()

st.title("User Dashboard")
st.write(f"Welcome, {st.session_state.user_email}!")

if st.button("Logout"):
    st.session_state.clear()
    st.set_query_params(page="welcome")
    st.stop()