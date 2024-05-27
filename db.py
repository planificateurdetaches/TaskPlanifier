from sqlalchemy import Column, String, Integer, DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///app.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tasks = relationship("Task", back_populates="owner")
    reset_token = Column(String, nullable=True)  # New field for the reset token

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    program_path = Column(String)
    scheduled_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="tasks")

Base.metadata.create_all(bind=engine)

def get_user(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

def add_task(title, description, program_path, scheduled_time, user_id):
    db = SessionLocal()
    task = Task(
        title=title,
        description=description,
        program_path=program_path,
        scheduled_time=scheduled_time,
        user_id=user_id
    )
    db.add(task)
    db.commit()
    db.close()

def get_tasks_by_user(user_id):
    db = SessionLocal()
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    db.close()
    return tasks

def get_username_by_email(email):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    if user:
        return user.username
    return None

