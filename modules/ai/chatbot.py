from modules.ai.tools import (
    get_pending_tasks,
    get_completed_tasks,
    get_today_schedule,
    get_upcoming_deadlines,
    get_productivity
)
from modules.ai.groq_service import ask_ai


def get_chatbot_response(prompt, task_text, timetable_text):
    """
    Generate a chatbot response using the Groq AI service.
    
    Args:
        prompt: User's question
        task_text: Formatted string of user's tasks
        timetable_text: Formatted string of user's timetable
    
    Returns:
        AI-generated response string
    """
    context = f"""
===== USER'S TASKS =====
{task_text}

===== USER'S TIMETABLE =====
{timetable_text}
"""
    
    return ask_ai(context, prompt)


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