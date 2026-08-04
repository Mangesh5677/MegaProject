from datetime import date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    Boolean,
)

from .database import Base


# ==========================================
# User Model
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    created_at = Column(Date, default=date.today)


# ==========================================
# Task Model
# ==========================================

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String)

    priority = Column(String)

    status = Column(String, default="Pending")

    due_date = Column(Date)

    due_time = Column(Time)

    # Duration (Minutes)
    duration = Column(Integer)

    # AI Scheduler
    scheduled_date = Column(Date, nullable=True)

    scheduled_start = Column(Time, nullable=True)

    scheduled_end = Column(Time, nullable=True)

    # Email Reminder
    email = Column(String, nullable=True)

    # Reminder Flags
    reminder_24h_sent = Column(Boolean, default=False)

    reminder_2h_sent = Column(Boolean, default=False)

    reminder_30m_sent = Column(Boolean, default=False)


# ==========================================
# Fixed Weekly Timetable
# ==========================================

class FixedSchedule(Base):
    __tablename__ = "fixed_schedule"

    id = Column(Integer, primary_key=True, index=True)

    day = Column(String, nullable=False)

    title = Column(String, nullable=False)

    category = Column(String)

    start_time = Column(Time)

    end_time = Column(Time)

    locked = Column(Boolean, default=True)


# ==========================================
# AI Generated Schedule
# ==========================================

class ScheduledTask(Base):
    __tablename__ = "scheduled_tasks"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer)

    title = Column(String)

    date = Column(Date)

    start_time = Column(Time)

    end_time = Column(Time)