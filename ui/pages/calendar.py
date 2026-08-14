import streamlit as st
from datetime import date, datetime, time

from modules.database.database import SessionLocal
from modules.database.crud import get_tasks


def render_calendar():

    st.title("📅 Calendar")

    user = st.session_state.user

    db = SessionLocal()

    try:

        # =====================================================
        # Get ONLY logged-in user's tasks
        # =====================================================

        tasks = get_tasks(
            db,
            user.id
        )

        # =====================================================
        # Calendar Date
        # =====================================================

        selected_date = st.date_input(
            "Select Date",
            value=date.today()
        )

        st.divider()

        st.subheader(
            f"📋 Tasks for {selected_date.strftime('%d %B %Y')}"
        )

        # =====================================================
        # Filter tasks for selected date
        # =====================================================

        selected_tasks = [
            task
            for task in tasks
            if task.due_date == selected_date
        ]

        # =====================================================
        # No Tasks
        # =====================================================

        if not selected_tasks:

            st.info(
                "📭 No tasks scheduled for this date."
            )

            return

        # =====================================================
        # Display Tasks
        # =====================================================

        for task in sorted(
            selected_tasks,
            key=lambda x: x.due_time or time(23, 59)
        ):

            if task.priority == "High":

                badge = "🔴 HIGH"

            elif task.priority == "Medium":

                badge = "🟡 MEDIUM"

            else:

                badge = "🟢 LOW"

            if task.status == "Completed":

                status = "✅ Completed"

            else:

                status = "⏳ Pending"

            due_time = (
                task.due_time.strftime("%H:%M")
                if task.due_time
                else "No time"
            )

            duration = (
                f"{task.duration} minutes"
                if task.duration
                else "Not specified"
            )

            st.markdown(
                f"""
                <div class="task-card">

                    <h3>📌 {task.title}</h3>

                    <p>
                        {task.description or "No description"}
                    </p>

                    <hr>

                    <b>{badge}</b>

                    <br><br>

                    🕒 Due Time:
                    <b>{due_time}</b>

                    <br>

                    ⏱ Duration:
                    <b>{duration}</b>

                    <br>

                    📌 Status:
                    <b>{status}</b>

                </div>
                """,
                unsafe_allow_html=True
            )

    finally:

        db.close()