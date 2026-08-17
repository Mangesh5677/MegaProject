import os
from datetime import date

from groq import Groq
from dotenv import load_dotenv


# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to your .env file."
    )


# ============================================================
# Groq Client
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# Current Groq Model
# ============================================================

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """
You are an AI Productivity Assistant inside an AI Productivity Manager.

Your job is to help the user manage:

1. Tasks
2. Deadlines
3. Priorities
4. Daily productivity
5. College timetable
6. Fixed schedules
7. Time management
8. Study planning
9. Task scheduling
10. Productivity advice

IMPORTANT RULES:

- Be friendly, concise and useful.
- Never invent tasks.
- Only use tasks provided in the context.
- Respect the user's fixed college timetable.
- Do not schedule tasks during fixed schedules.
- If the user asks what they should do today, prioritize:
  1. Overdue tasks
  2. High priority tasks
  3. Tasks due today
  4. Short tasks that can realistically be completed
- Clearly distinguish between Pending and Completed tasks.
- Use emojis naturally.
- Format responses using clean Markdown.
- Do NOT output HTML tags.
- Do NOT output raw Python code unless the user asks for code.
- Do NOT mention internal database details.
- If there are no tasks, tell the user clearly.
- If information is missing, ask a useful question.
"""


# ============================================================
# Build Context
# ============================================================

def build_productivity_context(tasks=None, fixed_schedules=None):
    """
    Convert database information into a clean context
    for the AI chatbot.
    """

    today = date.today()

    context = []

    context.append(
        f"Today's date: {today}"
    )

    # --------------------------------------------------------
    # Tasks
    # --------------------------------------------------------

    context.append("\nTASKS:")

    if tasks:

        for task in tasks:

            task_date = (
                str(task.due_date)
                if task.due_date
                else "No due date"
            )

            task_time = (
                str(task.due_time)
                if task.due_time
                else "No due time"
            )

            duration = (
                f"{task.duration} minutes"
                if getattr(task, "duration", None)
                else "Unknown duration"
            )

            context.append(
                f"""
- ID: {task.id}
  Title: {task.title}
  Description: {task.description or "No description"}
  Priority: {task.priority}
  Status: {task.status}
  Due Date: {task_date}
  Due Time: {task_time}
  Duration: {duration}
"""
            )

    else:

        context.append(
            "No tasks available."
        )

    # --------------------------------------------------------
    # Fixed Timetable
    # --------------------------------------------------------

    context.append(
        "\nFIXED COLLEGE / WEEKLY SCHEDULE:"
    )

    if fixed_schedules:

        for schedule in fixed_schedules:

            context.append(
                f"""
- {schedule.day}
  {schedule.title}
  Category: {schedule.category}
  Start: {schedule.start_time}
  End: {schedule.end_time}
"""
            )

    else:

        context.append(
            "No fixed schedule available."
        )

    return "\n".join(context)


# ============================================================
# Chatbot Response
# ============================================================

def get_chatbot_response(
    user_message,
    tasks=None,
    fixed_schedules=None,
    chat_history=None
):
    """
    Generate an AI response using Groq.
    """

    try:

        productivity_context = (
            build_productivity_context(
                tasks=tasks,
                fixed_schedules=fixed_schedules
            )
        )

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "system",
                "content": (
                    "Here is the user's current "
                    "productivity data:\n\n"
                    + productivity_context
                )
            }
        ]

        # ----------------------------------------------------
        # Previous Conversation
        # ----------------------------------------------------

        if chat_history:

            for message in chat_history[-10:]:

                role = message.get("role")
                content = message.get("content")

                if role in ["user", "assistant"] and content:

                    messages.append(
                        {
                            "role": role,
                            "content": content
                        }
                    )

        # ----------------------------------------------------
        # Current User Message
        # ----------------------------------------------------

        messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        # ----------------------------------------------------
        # Groq Request
        # ----------------------------------------------------

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.5,
            max_tokens=1200,
        )

        answer = (
            response.choices[0]
            .message
            .content
        )

        if not answer:

            return (
                "⚠️ I couldn't generate a response. "
                "Please try again."
            )

        return answer.strip()

    except Exception as e:

        error_message = str(e)

        # ----------------------------------------------------
        # Friendly Model Error
        # ----------------------------------------------------

        if (
            "model_not_found" in error_message
            or "does not exist" in error_message
        ):

            return (
                "⚠️ The AI model configured for the chatbot "
                "is currently unavailable.\n\n"
                "Please update the Groq model configuration."
            )

        # ----------------------------------------------------
        # Authentication Error
        # ----------------------------------------------------

        if (
            "401" in error_message
            or "authentication" in error_message.lower()
            or "api key" in error_message.lower()
        ):

            return (
                "🔑 Groq API authentication failed.\n\n"
                "Please check your `GROQ_API_KEY` "
                "in the `.env` file."
            )

        # ----------------------------------------------------
        # Rate Limit
        # ----------------------------------------------------

        if (
            "429" in error_message
            or "rate limit" in error_message.lower()
        ):

            return (
                "⏳ The AI service is temporarily busy.\n\n"
                "Please wait a few seconds and try again."
            )

        # ----------------------------------------------------
        # Generic Error
        # ----------------------------------------------------

        return (
            "❌ I couldn't generate a response right now.\n\n"
            f"Error: {error_message}"
        )