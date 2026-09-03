import streamlit as st

from modules.database.database import SessionLocal
from modules.dashboard.dashboard_service import get_dashboard_data


def card(title, value, icon):

    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard():

    user = st.session_state.user

    db = SessionLocal()

    try:

        # =====================================================
        # Get ONLY logged-in user's dashboard data
        # =====================================================

        data = get_dashboard_data(
            db,
            user.id
        )

        # =====================================================
        # Header
        # =====================================================

        st.title("AI Productivity Manager")
        st.caption(
            f"Welcome back, {user.name} 👋"
        )

        # =====================================================
        # Statistics
        # =====================================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            card(
                "Total Tasks",
                data["total"],
                "📋"
            )

        with c2:
            card(
                "Pending",
                data["pending"],
                "⏳"
            )

        with c3:
            card(
                "Completed",
                data["completed"],
                "✅"
            )

        with c4:
            card(
                "Productivity",
                f"{data['productivity']}%",
                "⚡"
            )

        # =====================================================
        # Timetable + Goal
        # =====================================================

        st.divider()

        left, right = st.columns([2, 1])

        # =====================================================
        # Today's Timetable
        # =====================================================

        with left:

            st.subheader("📅 Today's Timetable")

            if not data["today_classes"]:

                st.info(
                    "No classes scheduled for today."
                )

            else:

                for cls in data["today_classes"]:

                    start = (
                        cls.start_time.strftime("%I:%M %p")
                        if cls.start_time
                        else "--:--"
                    )

                    end = (
                        cls.end_time.strftime("%I:%M %p")
                        if cls.end_time
                        else "--:--"
                    )

                    st.markdown(
                        f"""
                        <div class="schedule-card">

                        🕒 <b>{start}</b>

                        ➜

                        <b>{end}</b>

                        <br><br>

                        📘 <b>{cls.title}</b>

                        <br>

                        📂 {cls.category or "Other"}

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # =====================================================
        # Today's Goal
        # =====================================================

        with right:

            st.subheader("🎯 Today's Goal")

            productivity = data["productivity"]

            st.progress(
                productivity / 100
            )

            st.write(
                f"### {productivity}% Completed"
            )

            if data["pending"] == 0:

                st.success(
                    "🎉 All tasks completed!"
                )

            else:

                st.warning(
                    f"{data['pending']} Task(s) Remaining"
                )

        # =====================================================
        # AI Recommendation
        # =====================================================

        st.divider()

        st.subheader("🤖 AI Recommendation")

        if data["pending"] == 0:

            st.success(
                "🎉 Great job! All your tasks are completed."
            )

        else:

            st.info(
                f"""
                Complete your **High Priority** tasks first.

                You currently have
                **{data['pending']} pending task(s)**.

                Use your available timetable slots efficiently.
                """
            )

    finally:

        db.close()