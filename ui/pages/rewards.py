import streamlit as st

from modules.database.database import SessionLocal
from modules.rewards.reward_service import (
    get_achievements,
    get_level_name,
    get_level_progress,
    get_or_create_reward,
)


LEVEL_TARGETS = {
    1: 100,
    2: 250,
    3: 500,
    4: 1000,
    5: 2000,
}


def _get_user_id():
    user = st.session_state.get("user")

    if hasattr(user, "id"):
        return user.id

    if isinstance(user, dict):
        return user.get("id")

    return None


def render_rewards():
    st.title("Rewards")
    st.caption("Track your productivity points, level, streaks, and achievements.")

    user_id = _get_user_id()

    if not user_id:
        st.error("Unable to identify the logged-in user.")
        return

    db = SessionLocal()

    try:
        reward = get_or_create_reward(db, user_id)
        achievements = get_achievements(reward)
        progress = get_level_progress(reward)

        st.subheader(get_level_name(reward.level))

        level_target = LEVEL_TARGETS.get(reward.level)

        if level_target:
            remaining_points = max(level_target - reward.points, 0)
            st.progress(progress / 100)
            st.caption(
                f"{reward.points} / {level_target} points · "
                f"{remaining_points} points until level {reward.level + 1}"
            )
        else:
            st.progress(1.0)
            st.caption(f"{reward.points} points · Maximum level reached")

        points_col, streak_col, tasks_col, perfect_col = st.columns(4)

        with points_col:
            st.metric("Points", reward.points)

        with streak_col:
            st.metric("Current streak", f"{reward.streak} days")

        with tasks_col:
            st.metric("Tasks completed", reward.tasks_completed)

        with perfect_col:
            st.metric("Perfect days", reward.perfect_days)

        st.divider()
        st.subheader("Achievements")

        unlocked_count = sum(
            achievement["unlocked"] for achievement in achievements
        )

        st.caption(
            f"{unlocked_count} of {len(achievements)} achievements unlocked"
        )

        columns = st.columns(2)

        for index, achievement in enumerate(achievements):
            with columns[index % 2]:
                with st.container(border=True):
                    if achievement["unlocked"]:
                        st.success(f"Unlocked — {achievement['title']}")
                    else:
                        st.info(f"Locked — {achievement['title']}")

                    st.caption(achievement["description"])

        st.divider()
        st.subheader("How to earn points")

        st.markdown(
            """
            - Low-priority task: **10 points**
            - Medium-priority task: **20 points**
            - High-priority task: **30 points**
            - Completing a task before its deadline: **+10 bonus points**
            - Streak bonuses: **3 days +30**, **7 days +100**, **30 days +500**
            """
        )

    except Exception as error:
        st.error(f"Unable to load rewards: {error}")

    finally:
        db.close()
import streamlit as st

from modules.database.database import SessionLocal
from modules.rewards.reward_service import (
    get_achievements,
    get_level_name,
    get_level_progress,
    get_or_create_reward,
)


LEVEL_TARGETS = {
    1: 100,
    2: 250,
    3: 500,
    4: 1000,
    5: 2000,
}


def _get_user_id():
    user = st.session_state.get("user")

    if hasattr(user, "id"):
        return user.id

    if isinstance(user, dict):
        return user.get("id")

    return None


def render_rewards():
    st.title("Rewards")
    st.caption("Track your productivity points, level, streaks, and achievements.")

    user_id = _get_user_id()

    if not user_id:
        st.error("Unable to identify the logged-in user.")
        return

    db = SessionLocal()

    try:
        reward = get_or_create_reward(db, user_id)
        achievements = get_achievements(reward)
        progress = get_level_progress(reward)

        st.subheader(get_level_name(reward.level))

        level_target = LEVEL_TARGETS.get(reward.level)
        if level_target:
            remaining_points = max(level_target - reward.points, 0)
            st.progress(progress / 100)
            st.caption(
                f"{reward.points} / {level_target} points · "
                f"{remaining_points} points until level {reward.level + 1}"
            )
        else:
            st.progress(1.0)
            st.caption(f"{reward.points} points · Maximum level reached")

        points_col, streak_col, tasks_col, perfect_col = st.columns(4)
        points_col.metric("Points", reward.points)
        streak_col.metric("Current streak", f"{reward.streak} days")
        tasks_col.metric("Tasks completed", reward.tasks_completed)
        perfect_col.metric("Perfect days", reward.perfect_days)

        st.divider()
        st.subheader("Achievements")

        unlocked_count = sum(item["unlocked"] for item in achievements)
        st.caption(f"{unlocked_count} of {len(achievements)} achievements unlocked")

        columns = st.columns(2)
        for index, achievement in enumerate(achievements):
            with columns[index % 2]:
                with st.container(border=True):
                    status = "Unlocked" if achievement["unlocked"] else "Locked"
                    st.write(f"**{status}: {achievement['title']}**")
                    st.caption(achievement["description"])

        st.divider()
        st.subheader("How to earn points")
        st.markdown(
            """
            - Low-priority task: **10 points**
            - Medium-priority task: **20 points**
            - High-priority task: **30 points**
            - Completing a task before its deadline: **+10 points**
            - Streak bonuses: **3 days +30**, **7 days +100**, **30 days +500**
            """
        )

    except Exception as error:
        st.error(f"Unable to load rewards: {error}")

    finally:
        db.close()
