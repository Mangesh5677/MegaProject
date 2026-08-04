import time

from modules.database.database import SessionLocal
from modules.notifications.reminder_service import check_reminders

print("📧 Reminder Service Started...")

while True:

    db = SessionLocal()

    try:
        check_reminders(db)
    except Exception as e:
        print("❌ Error:", e)
    finally:
        db.close()

    # Check every minute
    time.sleep(60)