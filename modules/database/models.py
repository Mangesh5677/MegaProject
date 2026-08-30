from datetime import date, datetime

from altair import DateTime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Time,
    Boolean,
    ForeignKey,
    Text,
)

from .database import Base


# ============================================================
# User Model
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================================
# Settings Model
# ============================================================

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    # -------------------------
    # Notifications
    # -------------------------

    email_notification = Column(Boolean, default=True)

    desktop_notification = Column(Boolean, default=True)

    reminder_24h = Column(Boolean, default=True)

    reminder_2h = Column(Boolean, default=True)

    reminder_30m = Column(Boolean, default=True)

    # -------------------------
    # AI Settings
    # -------------------------

    ai_model = Column(
        String,
        default="llama-3.3-70b-versatile"
    )

    temperature = Column(
        String,
        default="0.4"
    )

    max_tokens = Column(
        Integer,
        default=600
    )

    # -------------------------
    # Scheduler
    # -------------------------

    work_start = Column(
        Time,
        nullable=True
    )

    work_end = Column(
        Time,
        nullable=True
    )

    daily_hours = Column(
        Integer,
        default=6
    )


# ============================================================
# Task Model
# ============================================================

class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # IMPORTANT:
    # Every task belongs to a user

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(String)

    priority = Column(String)

    status = Column(
        String,
        default="Pending"
    )

    due_date = Column(Date)

    due_time = Column(Time)

    # Duration in minutes

    duration = Column(Integer)

    task_type = Column(
        String,
        default="Once"
    )

    # -------------------------
    # AI Scheduler
    # -------------------------

    scheduled_date = Column(
        Date,
        nullable=True
    )

    scheduled_start = Column(
        Time,
        nullable=True
    )

    scheduled_end = Column(
        Time,
        nullable=True
    )

    # -------------------------
    # Email
    # -------------------------

    email = Column(
        String,
        nullable=True
    )

    # -------------------------
    # Reminder Flags
    # -------------------------

    reminder_24h_sent = Column(
        Boolean,
        default=False
    )

    reminder_2h_sent = Column(
        Boolean,
        default=False
    )

    reminder_30m_sent = Column(
        Boolean,
        default=False
    )


# ============================================================
# Fixed Weekly Timetable
# ============================================================

class FixedSchedule(Base):
    __tablename__ = "fixed_schedule"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # IMPORTANT:
    # Every timetable entry belongs to a user

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    day = Column(
        String,
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    category = Column(String)

    start_time = Column(Time)

    end_time = Column(Time)

    locked = Column(
        Boolean,
        default=True
    )


# ============================================================
# AI Generated Schedule
# ============================================================

class ScheduledTask(Base):
    __tablename__ = "scheduled_tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # User ownership

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    task_id = Column(Integer)

    title = Column(String)

    date = Column(Date)

    start_time = Column(Time)

    end_time = Column(Time)


# ============================================================
# INTERNSHIP MODEL
# ============================================================

class Internship(Base):
    __tablename__ = "internships"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Owner of internship record

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # -------------------------
    # Internship Information
    # -------------------------

    company_name = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    location = Column(
        String,
        nullable=True
    )

    work_mode = Column(
        String,
        nullable=True
    )

    # Example:
    # Remote / Hybrid / On-site

    skills = Column(
        Text,
        nullable=True
    )

    # -------------------------
    # Dates
    # -------------------------

    application_deadline = Column(
        Date,
        nullable=True
    )

    interview_date = Column(
        Date,
        nullable=True
    )

    # -------------------------
    # Link
    # -------------------------

    application_url = Column(
        String,
        nullable=True
    )

    # -------------------------
    # Status
    # -------------------------

    status = Column(
        String,
        default="Saved"
    )

    # Saved
    # Preparing
    # Applied
    # Interview
    # Selected
    # Rejected


# ============================================================
# INTERNSHIP APPLICATION MODEL
# ============================================================

class InternshipApplication(Base):
    __tablename__ = "internship_applications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # User ownership

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Related internship

    internship_id = Column(
        Integer,
        ForeignKey("internships.id"),
        nullable=False,
        index=True
    )

    # -------------------------
    # Application Details
    # -------------------------

    applied_date = Column(
        Date,
        nullable=True
    )

    status = Column(
        String,
        default="Applied"
    )

    # Applied
    # Shortlisted
    # Interview
    # Selected
    # Rejected

    interview_date = Column(
        Date,
        nullable=True
    )

    notes = Column(
        Text,
        nullable=True
    )


# ============================================================
# INTERNSHIP PREPARATION TASK
# ============================================================

class PreparationTask(Base):
    __tablename__ = "preparation_tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # User ownership

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Related internship

    internship_id = Column(
        Integer,
        ForeignKey("internships.id"),
        nullable=False,
        index=True
    )

    # -------------------------
    # Preparation Information
    # -------------------------

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    category = Column(
        String,
        nullable=True
    )

    # Example:
    # Java
    # DSA
    # SQL
    # Aptitude
    # HR
    # Interview

    priority = Column(
        String,
        default="Medium"
    )

    duration = Column(
        Integer,
        default=30
    )

    # -------------------------
    # Schedule
    # -------------------------

    preparation_date = Column(
        Date,
        nullable=True
    )

    completed = Column(
        Boolean,
        default=False
    )


# ============================================================
# REWARDS MODEL
# ============================================================

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Every reward belongs to one user
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # -------------------------
    # Reward Information
    # -------------------------

    points = Column(
        Integer,
        default=0
    )

    level = Column(
        Integer,
        default=1
    )

    streak = Column(
        Integer,
        default=0
    )

    tasks_completed = Column(
        Integer,
        default=0
    )

    perfect_days = Column(
        Integer,
        default=0
    )

    last_completion_date = Column(
        Date,
        nullable=True
    )

    reason = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

# ============================================================
# USER REWARD SUMMARY
# ============================================================

class UserReward(Base):
    __tablename__ = "user_rewards"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        index=True
    )

    total_points = Column(
        Integer,
        default=0
    )

    current_streak = Column(
        Integer,
        default=0
    )

    longest_streak = Column(
        Integer,
        default=0
    )