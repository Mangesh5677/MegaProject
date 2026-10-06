
from modules.database.database import SessionLocal
from modules.analytics.activity_service import (
    get_all_users,
    get_admin_user_stats,
    get_recent_activities,
)

db = SessionLocal()

try:
    users = get_all_users(db)
    stats = get_admin_user_stats(db)
    activities = get_recent_activities(db)

    print("Registered users:", len(users))
    print("User statistics:", stats)
    print("Recent activity records:", len(activities))

finally:
    db.close()