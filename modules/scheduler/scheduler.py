from modules.database.models import Task, FixedSchedule


def generate_schedule(db):
    tasks = (
        db.query(Task)
        .filter(Task.status == "Pending")
        .order_by(Task.priority.desc())
        .all()
    )

    fixed_events = db.query(FixedSchedule).all()

    if not tasks:
        return "No pending tasks found."

    if not fixed_events:
        return "No fixed timetable found."

    suggestions = []

    for task in tasks:
        suggestions.append({
            "task": task.title,
            "duration": task.duration,
            "status": "Ready to Schedule"
        })

    return suggestions