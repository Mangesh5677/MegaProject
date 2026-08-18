from datetime import date, timedelta

from modules.database.models import Reward


# ==========================================
# Get or Create Reward
# ==========================================

def get_or_create_reward(db, user_id):

    reward = (
        db.query(Reward)
        .filter(
            Reward.user_id == user_id
        )
        .first()
    )

    if reward is None:

        reward = Reward(
            user_id=user_id,
            points=0,
            level=1,
            streak=0,
            tasks_completed=0,
            perfect_days=0,
            last_completion_date=None,
        )

        db.add(reward)
        db.commit()
        db.refresh(reward)

    return reward


# ==========================================
# Calculate Level
# ==========================================

def calculate_level(points):

    if points >= 2000:
        return 6

    elif points >= 1000:
        return 5

    elif points >= 500:
        return 4

    elif points >= 250:
        return 3

    elif points >= 100:
        return 2

    return 1


# ==========================================
# Level Name
# ==========================================

def get_level_name(level):

    levels = {
        1: "🌱 Beginner",
        2: "🚀 Starter",
        3: "⚡ Productive",
        4: "🏅 Achiever",
        5: "🔥 Pro",
        6: "👑 Productivity Master",
    }

    return levels.get(
        level,
        "🌱 Beginner"
    )


# ==========================================
# Award Task Completion
# ==========================================

def award_task_completion(
    db,
    user_id,
    priority="Low",
    completed_before_deadline=False,
):

    reward = get_or_create_reward(
        db,
        user_id
    )

    # --------------------------------------
    # Points Based On Priority
    # --------------------------------------

    if priority == "High":

        earned_points = 30

    elif priority == "Medium":

        earned_points = 20

    else:

        earned_points = 10

    # --------------------------------------
    # Deadline Bonus
    # --------------------------------------

    if completed_before_deadline:

        earned_points += 10

    reward.points += earned_points

    reward.tasks_completed += 1

    # --------------------------------------
    # Streak
    # --------------------------------------

    today = date.today()

    if reward.last_completion_date:

        yesterday = today - timedelta(days=1)

        if reward.last_completion_date == today:

            # Already completed a task today.
            # Don't increase streak again.
            pass

        elif reward.last_completion_date == yesterday:

            reward.streak += 1

        else:

            reward.streak = 1

    else:

        reward.streak = 1

    reward.last_completion_date = today

    # --------------------------------------
    # Streak Bonus
    # --------------------------------------

    if reward.streak == 3:

        reward.points += 30

    elif reward.streak == 7:

        reward.points += 100

    elif reward.streak == 30:

        reward.points += 500

    # --------------------------------------
    # Calculate Level
    # --------------------------------------

    reward.level = calculate_level(
        reward.points
    )

    db.commit()
    db.refresh(reward)

    return reward, earned_points


# ==========================================
# Level Progress
# ==========================================

def get_level_progress(reward):

    levels = {
        1: (0, 100),
        2: (100, 250),
        3: (250, 500),
        4: (500, 1000),
        5: (1000, 2000),
        6: (2000, 2000),
    }

    current_points, next_points = levels.get(
        reward.level,
        (0, 100)
    )

    # Maximum level
    if reward.level >= 6:

        return 100

    progress = (
        (reward.points - current_points)
        /
        (next_points - current_points)
    ) * 100

    return max(
        0,
        min(
            100,
            round(progress)
        )
    )


# ==========================================
# Achievements
# ==========================================

def get_achievements(reward):

    achievements = []

    # --------------------------------------
    # First Step
    # --------------------------------------

    achievements.append({
        "title": "🥉 First Step",
        "description": "Complete your first task.",
        "unlocked": reward.tasks_completed >= 1,
    })

    # --------------------------------------
    # Getting Started
    # --------------------------------------

    achievements.append({
        "title": "🥈 Getting Started",
        "description": "Complete 10 tasks.",
        "unlocked": reward.tasks_completed >= 10,
    })

    # --------------------------------------
    # Productivity Master
    # --------------------------------------

    achievements.append({
        "title": "🥇 Productivity Master",
        "description": "Complete 50 tasks.",
        "unlocked": reward.tasks_completed >= 50,
    })

    # --------------------------------------
    # 7 Day Streak
    # --------------------------------------

    achievements.append({
        "title": "🔥 7 Day Streak",
        "description": "Maintain a 7-day productivity streak.",
        "unlocked": reward.streak >= 7,
    })

    # --------------------------------------
    # 30 Day Streak
    # --------------------------------------

    achievements.append({
        "title": "👑 30 Day Streak",
        "description": "Maintain a 30-day productivity streak.",
        "unlocked": reward.streak >= 30,
    })

    # --------------------------------------
    # 1000 Points
    # --------------------------------------

    achievements.append({
        "title": "💯 1000 Points",
        "description": "Earn 1000 productivity points.",
        "unlocked": reward.points >= 1000,
    })

    return achievements