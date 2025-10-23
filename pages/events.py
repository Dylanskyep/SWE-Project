import streamlit as st
from services.event_service import get_upcoming_events

st.set_page_config(page_title="Events", page_icon="📅")
st.title("Upcoming Events")

events = get_upcoming_events()

if not events:
    st.info("No upcoming events yet.")
else:
    for event_id, event in events:
        with st.container(border=True):
            st.subheader(event.get("title", "Untitled Event"))
            st.caption(f"{event.get('date', 'TBD')} • {event.get('time', '')} • {event.get('location', 'TBD')}")
            st.write(event.get("description", ""))
            st.write(f"Spots remaining: **{int(event.get('capacity', 0))}**")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Details", key=f"open_{event_id}"):
                    st.query_params["eid"] = event_id
                    try:
                        st.switch_page("pages/event_detail.py")
                    except Exception:
                        st.info("Open the 'Event Detail' page from the sidebar.")
            # with col2:
            #     st.caption(f"Event ID: `{event_id}`")