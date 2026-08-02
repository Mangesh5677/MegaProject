from modules.database.models import Task


def get_statistics(db):

    tasks = db.query(Task).all()

    total = len(tasks)

    completed = len(
        [t for t in tasks if t.status == "Completed"]
    )

    pending = total - completed

    productivity = 0

    if total != 0:
        productivity = round((completed / total) * 100)

    high = len([t for t in tasks if t.priority == "High"])
    medium = len([t for t in tasks if t.priority == "Medium"])
    low = len([t for t in tasks if t.priority == "Low"])

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "productivity": productivity,
        "priority": [high, medium, low]
    }