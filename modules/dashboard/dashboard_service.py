from datetime import date

from modules.database.models import Task, FixedSchedule


def get_dashboard_data(db, user_id):

    # ========================================================
    # Get ONLY logged-in user's tasks
    # ========================================================

    tasks = (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .all()
    )

    total = len(tasks)

    completed = len(
        [
            task
            for task in tasks
            if task.status == "Completed"
        ]
    )

    pending = len(
        [
            task
            for task in tasks
            if task.status == "Pending"
        ]
    )

    # ========================================================
    # Productivity
    # ========================================================

    productivity = 0

    if total > 0:
        productivity = round(
            (completed / total) * 100
        )

    # ========================================================
    # Today's day
    # ========================================================

    today = date.today().strftime("%A")

    # ========================================================
    # Get ONLY logged-in user's timetable
    # ========================================================

    today_classes = (
        db.query(FixedSchedule)
        .filter(
            FixedSchedule.user_id == user_id,
            FixedSchedule.day == today,
        )
        .order_by(
            FixedSchedule.start_time
        )
        .all()
    )

    # ========================================================
    # Return dashboard data
    # ========================================================

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "productivity": productivity,
        "today_classes": today_classes,
    }