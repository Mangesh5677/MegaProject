from apscheduler.schedulers.background import BackgroundScheduler

from modules.database.database import SessionLocal
from modules.notifications.reminder_service import check_reminders

scheduler = BackgroundScheduler()


def run_job():

    db = SessionLocal()

    try:
        check_reminders(db)

    except Exception as e:
        print(f"❌ Reminder Error: {e}")

    finally:
        db.close()


def start_scheduler():

    if scheduler.running:
        return

    scheduler.add_job(
        run_job,
        trigger="interval",
        minutes=1,
        id="email_scheduler",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    print("✅ Reminder Scheduler Started")