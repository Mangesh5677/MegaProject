from datetime import date
from modules.database.models import Task, FixedSchedule


def get_today_schedule(db):

    today = date.today()
    weekday = today.strftime("%A")

    fixed = (
        db.query(FixedSchedule)
        .filter(FixedSchedule.day == weekday)
        .order_by(FixedSchedule.start_time)
        .all()
    )

    tasks = (
        db.query(Task)
        .filter(Task.scheduled_date == today)
        .order_by(Task.scheduled_start)
        .all()
    )

    return fixed, tasks