import streamlit as st
from datetime import datetime
from db import add_task, get_user

def create_task_page():
    if not st.session_state.get('authenticated'):
        st.error("You must be logged in to view this page.")
        st.stop()

    username = st.session_state['user']['username']
    st.title(f"Create Task for {username}")

    user = get_user(username)
    if not user:
        st.error("User not found")
        return

    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    program_path = st.text_input("Program Path")
    scheduled_date = st.date_input("Scheduled Date", datetime.now().date())
    scheduled_time = st.time_input("Scheduled Time", datetime.now().time())
    scheduled_datetime = datetime.combine(scheduled_date, scheduled_time)

    if st.button("Create Task"):
        add_task(title, description, program_path, scheduled_datetime, user.id)
        st.success("Task created successfully")

# Sample usage in main app
if __name__ == "__main__":
    create_task_page()
