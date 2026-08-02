from datetime import date

from modules.database.models import Task, FixedSchedule


def get_pending_tasks(db):
    return (
        db.query(Task)
        .filter(Task.status == "Pending")
        .all()
    )


def get_completed_tasks(db):
    return (
        db.query(Task)
        .filter(Task.status == "Completed")
        .all()
    )


def get_today_schedule(db):

    today = date.today().strftime("%A")

    return (
        db.query(FixedSchedule)
        .filter(FixedSchedule.day == today)
        .order_by(FixedSchedule.start_time)
        .all()
    )


def get_upcoming_deadlines(db):

    today = date.today()

    return (
        db.query(Task)
        .filter(Task.due_date >= today)
        .order_by(Task.due_date)
        .limit(5)
        .all()
    )


def get_productivity(db):

    tasks = db.query(Task).all()

    total = len(tasks)

    completed = len(
        [t for t in tasks if t.status == "Completed"]
    )

    pending = total - completed

    productivity = (
        round((completed / total) * 100)
        if total else 0
    )

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "productivity": productivity,
    }