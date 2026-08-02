from sqlalchemy import Column, Integer, String, Date, Time, Boolean
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String)

    priority = Column(String)

    status = Column(String, default="Pending")

    due_date = Column(Date)
    due_time = Column(Time)

    # AI Scheduler Fields
    duration = Column(Integer)
    scheduled_date = Column(Date, nullable=True)
    scheduled_start = Column(Time, nullable=True)
    scheduled_end = Column(Time, nullable=True)

    # Email Reminder
    email = Column(String, nullable=True)
    reminder_sent = Column(Boolean, default=False)


class FixedSchedule(Base):
    __tablename__ = "fixed_schedule"

    id = Column(Integer, primary_key=True, index=True)

    day = Column(String, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String)

    start_time = Column(Time)
    end_time = Column(Time)

    locked = Column(Boolean, default=True)