from datetime import datetime

from modules.database.models import Task
from modules.notifications.email_service import send_email
from modules.notifications.desktop_notification import show_notification


def send_task_email(task, subject, body):
    """
    Send reminder email.
    """
    send_email(
        task.email,
        subject,
        body
    )


def check_reminders(db):

    now = datetime.now()

    print("=" * 60)
    print("Checking reminders:", now.strftime("%Y-%m-%d %H:%M:%S"))

    tasks = (
        db.query(Task)
        .filter(Task.status == "Pending")
        .all()
    )

    print(f"Found {len(tasks)} pending task(s).")

    for task in tasks:

        if not task.email:
            continue

        deadline = datetime.combine(
            task.due_date,
            task.due_time
        )

        remaining = (deadline - now).total_seconds()

        print("-----------------------------------------")
        print("Task:", task.title)
        print("Deadline:", deadline)
        print("Remaining:", round(remaining / 60), "minutes")

        if remaining <= 0:
            print("Deadline already passed.")
            continue

        # ==========================================
        # 24 HOURS REMINDER
        # ==========================================

        if (
            remaining <= 86400
            and not task.reminder_24h_sent
        ):

            subject = f"📅 24 Hour Reminder - {task.title}"

            body = f"""
Hello,

This is a reminder from AI Productivity Manager.

Your task is due within 24 hours.

Task:
{task.title}

Description:
{task.description}

Priority:
{task.priority}

Deadline:
{task.due_date}
{task.due_time}

Good luck!
"""

            send_task_email(task, subject, body)

            show_notification(
                title="📅 24 Hour Reminder",
                message=f"{task.title}\nDeadline: {task.due_time}"
            )

            task.reminder_24h_sent = True
            db.commit()

            print("✅ 24 Hour Reminder Sent")

        # ==========================================
        # 2 HOURS REMINDER
        # ==========================================

        elif (
            remaining <= 7200
            and not task.reminder_2h_sent
        ):

            subject = f"⏰ 2 Hour Reminder - {task.title}"

            body = f"""
Hello,

Only 2 hours are left before your deadline.

Task:
{task.title}

Description:
{task.description}

Priority:
{task.priority}

Deadline:
{task.due_date}
{task.due_time}

Please start working on it now.
"""

            send_task_email(task, subject, body)

            show_notification(
                title="⏰ 2 Hour Reminder",
                message=f"{task.title}\nDeadline: {task.due_time}"
            )

            task.reminder_2h_sent = True
            db.commit()

            print("✅ 2 Hour Reminder Sent")

        # ==========================================
        # 30 MINUTES REMINDER
        # ==========================================

        elif (
            remaining <= 1800
            and not task.reminder_30m_sent
        ):

            subject = f"🚨 Final Reminder - {task.title}"

            body = f"""
Hello,

Only 30 minutes remain before your deadline.

Task:
{task.title}

Description:
{task.description}

Priority:
{task.priority}

Deadline:
{task.due_date}
{task.due_time}

Please complete your task immediately.

AI Productivity Manager
"""

            send_task_email(task, subject, body)

            show_notification(
                title="🚨 Final Reminder",
                message=f"{task.title}\nOnly 30 minutes remaining!"
            )

            task.reminder_30m_sent = True
            db.commit()

            print("✅ 30 Minute Reminder Sent")

        else:

            hours = round(remaining / 3600, 2)
            print(f"Waiting... {hours} hour(s) remaining")