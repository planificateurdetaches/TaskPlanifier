import streamlit as st
from session_state import get_user_session
from db import SessionLocal, Task
from scheduler import scheduler, schedule_task
from datetime import datetime

def modify_task_page():
    user_session = get_user_session()
    if not st.session_state.get('authenticated'):
        st.error("You must be logged in to view this page.")
        st.stop()
    
    user_id = st.session_state['user']['id']
    db = SessionLocal()
    tasks = db.query(Task).filter(Task.user_id == user_session['user']['id']).all()
    task_options = {task.id: f"Task {task.id} - {task.program_path}" for task in tasks}
    task_id = st.selectbox("Select Task", list(task_options.keys()), format_func=lambda x: task_options[x])
    selected_task = db.query(Task).filter(Task.id == task_id).first()

    if selected_task:
        new_program_path = st.text_input("Program Path", value=selected_task.program_path)
        new_run_date = st.date_input("Run Date", value=selected_task.scheduled_time.date())
        new_run_time = st.time_input("Run Time", value=selected_task.scheduled_time.time())
        new_run_datetime = datetime.combine(new_run_date, new_run_time)

        if st.button("Modify Task"):
            selected_task.program_path = new_program_path
            selected_task.scheduled_time = new_run_datetime
            db.commit()
            
            # Remove the old job and add a new one
            scheduler.remove_job(str(task_id))
            schedule_task(task_id, new_program_path, new_run_datetime)
            
            st.success("Task modified successfully")
    db.close()

# Sample usage in main app
if __name__ == "__main__":
    modify_task_page()


