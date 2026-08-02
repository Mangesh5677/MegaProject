from modules.ai.tools import (
    get_pending_tasks,
    get_completed_tasks,
    get_today_schedule,
    get_upcoming_deadlines,
    get_productivity
)


def build_context(db):

    stats = get_productivity(db)

    context = ""

    context += "===== PRODUCTIVITY =====\n"

    context += f"""
Total Tasks : {stats['total']}
Completed : {stats['completed']}
Pending : {stats['pending']}
Productivity : {stats['productivity']}%
"""

    context += "\n===== PENDING TASKS =====\n"

    for task in get_pending_tasks(db):

        context += f"""
Task : {task.title}
Priority : {task.priority}
Deadline : {task.due_date}
Duration : {task.duration} minutes

"""

    context += "\n===== TODAY'S TIMETABLE =====\n"

    for event in get_today_schedule(db):

        context += f"""
{event.start_time} - {event.end_time}
{event.title}
"""

    context += "\n===== UPCOMING DEADLINES =====\n"

    for task in get_upcoming_deadlines(db):

        context += f"""
{task.title}
Deadline : {task.due_date}
"""

    return context