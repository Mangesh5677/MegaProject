from datetime import datetime

from modules.database.activity import UserActivity


def log_activity(
    db,
    user_id,
    activity_type,
    activity_details=None
):
    activity = UserActivity(
        user_id=user_id,
        activity_type=activity_type,
        activity_details=activity_details,
        created_at=datetime.utcnow()
    )

    db.add(activity)
    db.commit()

    return activity


def get_user_activities(
    db,
    user_id,
    limit=100
):
    return (
        db.query(UserActivity)
        .filter(
            UserActivity.user_id == user_id
        )
        .order_by(
            UserActivity.created_at.desc()
        )
        .limit(limit)
        .all()
    )


def get_user_activity_count(
    db,
    user_id
):
    return (
        db.query(UserActivity)
        .filter(
            UserActivity.user_id == user_id
        )
        .count()
    )


def get_activity_count_by_type(
    db,
    user_id,
    activity_type
):
    return (
        db.query(UserActivity)
        .filter(
            UserActivity.user_id == user_id,
            UserActivity.activity_type == activity_type
        )
        .count()
    )


from sqlalchemy import func

from modules.database.models import User, Task
from modules.database.activity import UserActivity


def get_all_users(db):
    """Return all registered users."""
    return (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )


def get_admin_user_stats(db):
    """Return activity statistics for every user."""
    users = get_all_users(db)
    stats = []

    for user in users:
        activities = (
            db.query(
                UserActivity.activity_type,
                func.count(UserActivity.id),
            )
            .filter(UserActivity.user_id == user.id)
            .group_by(UserActivity.activity_type)
            .all()
        )

        activity_counts = dict(activities)

        stats.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": getattr(user, "role", "user"),
            "registered_at": user.created_at,
            "total_logins": activity_counts.get("LOGIN", 0),
            "chatbot_uses": activity_counts.get("AI_CHAT", 0),
            "scheduler_uses": activity_counts.get("AI_SCHEDULER", 0),
            "tasks_created": activity_counts.get("TASK_CREATED", 0),
            "tasks_completed": activity_counts.get("TASK_COMPLETED", 0),
            "total_activities": sum(activity_counts.values()),
        })

    return stats


def get_recent_activities(db, limit=50):
    """Return the most recent recorded activities."""
    return (
        db.query(UserActivity, User)
        .join(User, User.id == UserActivity.user_id)
        .order_by(UserActivity.created_at.desc())
        .limit(limit)
        .all()
    )