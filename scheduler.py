from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from db import SessionLocal, Task, User

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.start()

def schedule_task(task_id, program_path, run_time):
    scheduler.add_job(
        run_task,
        'date',
        run_date=run_time,
        args=[task_id, program_path],
        id=str(task_id)
    )

def run_task(task_id, program_path):
    subprocess.Popen([program_path])

def load_tasks_from_db():
    db = SessionLocal()
    tasks = db.query(Task).all()
    for task in tasks:
        schedule_task(task.id, task.program_path, task.run_time)
    db.close()

