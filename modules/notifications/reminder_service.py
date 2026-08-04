from datetime import datetime

from modules.database.models import Task
from modules.notifications.email_service import send_email


def send_task_email(task, subject, body):
    """
    Send email for a task.
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

        print("--------------------------------")
        print("Task:", task.title)
        print("Remaining:", round(remaining / 60), "minutes")

        if remaining <= 0:
            continue

        # ==========================
        # 24 Hour Reminder
        # ==========================

        if (
            remaining <= 86400
            and not task.reminder_24h_sent
        ):

            send_task_email(
                task,
                f"📅 Reminder (24 Hours): {task.title}",
                f"""
Hello,

Your task is due in less than 24 hours.

Task:
{task.title}

Deadline:
{task.due_date} {task.due_time}

Priority:
{task.priority}

AI Productivity Manager
"""
            )

            task.reminder_24h_sent = True
            db.commit()

            print("✅ 24 Hour Reminder Sent")

        # ==========================
        # 2 Hour Reminder
        # ==========================

        elif (
            remaining <= 7200
            and not task.reminder_2h_sent
        ):

            send_task_email(
                task,
                f"⏰ Reminder (2 Hours): {task.title}",
                f"""
Hello,

Only 2 hours remaining.

Task:
{task.title}

Deadline:
{task.due_date} {task.due_time}

Priority:
{task.priority}

AI Productivity Manager
"""
            )

            task.reminder_2h_sent = True
            db.commit()

            print("✅ 2 Hour Reminder Sent")

        # ==========================
        # 30 Minute Reminder
        # ==========================

        elif (
            remaining <= 1800
            and not task.reminder_30m_sent
        ):

            send_task_email(
                task,
                f"🚨 Reminder (30 Minutes): {task.title}",
                f"""
Hello,

Only 30 minutes left.

Task:
{task.title}

Deadline:
{task.due_date} {task.due_time}

Priority:
{task.priority}

Please complete it immediately.

AI Productivity Manager
"""
            )

            task.reminder_30m_sent = True
            db.commit()

            print("✅ 30 Minute Reminder Sent")

        else:

            print("Waiting...")