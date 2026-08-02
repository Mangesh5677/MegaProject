from datetime import date

from modules.database.models import Task, FixedSchedule


def get_dashboard_data(db):

    tasks = db.query(Task).all()

    total = len(tasks)

    completed = len(
        [t for t in tasks if t.status == "Completed"]
    )

    pending = total - completed

    productivity = 0

    if total > 0:
        productivity = round((completed / total) * 100)

    today = date.today().strftime("%A")

    today_classes = (
        db.query(FixedSchedule)
        .filter(FixedSchedule.day == today)
        .order_by(FixedSchedule.start_time)
        .all()
    )

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "productivity": productivity,
        "today_classes": today_classes
    }