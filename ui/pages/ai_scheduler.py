from turtle import color

from langgraph.func import task
import streamlit as st

from modules.database.database import SessionLocal
from modules.database.crud import get_tasks
from modules.ai.scheduler import generate_schedule


def render_ai_scheduler():

    st.title("🤖 AI Smart Scheduler")

    st.markdown(
        """
        The AI Scheduler automatically plans your pending tasks
        based on:

        - 🎓 Fixed College Timetable
        - ⭐ Task Priority
        - 📅 Deadline
        - ⏱ Task Duration
        """
    )

    user = st.session_state.user

    db = SessionLocal()

    try:

        # =====================================================
        # Generate Schedule
        # =====================================================

        col1, col2 = st.columns([1, 1])

        with col1:

            if st.button(
                "🚀 Generate AI Schedule",
                use_container_width=True
            ):

                with st.spinner(
                    "🤖 Generating your personalized schedule..."
                ):

                    scheduled, unscheduled = generate_schedule(
                        db,
                        user.id
                    )

                st.success(
                    f"✅ {len(scheduled)} task(s) scheduled successfully."
                )

                if unscheduled:

                    st.warning(
                        f"⚠️ {len(unscheduled)} task(s) could not be scheduled."
                    )

                    with st.expander(
                        "View Unscheduled Tasks"
                    ):

                        for task in unscheduled:

                            st.write(
                                f"• {task.title}"
                            )

        with col2:

            if st.button(
                "🔄 Refresh",
                use_container_width=True
            ):

                st.rerun()

        st.divider()

        # =====================================================
        # Get ONLY current user's tasks
        # =====================================================

        tasks = get_tasks(
            db,
            user.id
        )

        # =====================================================
        # Today's AI Schedule
        # =====================================================

        st.subheader(
            "📅 Your AI Schedule"
        )

        scheduled_tasks = [
            task
            for task in tasks
            if task.scheduled_start is not None
        ]

        # =====================================================
        # No Schedule
        # =====================================================

        if not scheduled_tasks:

            st.info(
                """
                📭 No tasks scheduled yet.

                Click **Generate AI Schedule** to create
                your personalized schedule.
                """
            )

            return

        # =====================================================
        # Sort by date and start time
        # =====================================================

        scheduled_tasks.sort(
            key=lambda task: (
                task.scheduled_date or task.due_date,
                task.scheduled_start
            )
        )

        # =====================================================
        # Display Schedule
        # =====================================================

        for task in scheduled_tasks:

            # -------------------------------------------------
            # Priority
            # -------------------------------------------------

            if task.priority == "High":

                color = "#ef4444"
                badge = "🔴 HIGH"

            elif task.priority == "Medium":

                color = "#f59e0b"
                badge = "🟡 MEDIUM"

            else:

                color = "#22c55e"
                badge = "🟢 LOW"

            # -------------------------------------------------
            # Status
            # -------------------------------------------------

            if task.status == "Completed":

                status = "✅ Completed"

            else:

                status = "⏳ Pending"

            # -------------------------------------------------
            # Date
            # -------------------------------------------------

            scheduled_date = (
                task.scheduled_date
                if task.scheduled_date
                else "-"
            )

            # -------------------------------------------------
            # Time
            # -------------------------------------------------

            start_time = (
                task.scheduled_start.strftime("%H:%M")
                if task.scheduled_start
                else "--:--"
            )

            end_time = (
                task.scheduled_end.strftime("%H:%M")
                if task.scheduled_end
                else "--:--"
            )
# -------------------------------------------------
# Display Card
# -------------------------------------------------

        with st.container(border=True):

          st.subheader(f"📌 {task.title}")

          st.write(
          task.description or "No Description"
         )

          st.divider()

          st.markdown(f"**{badge}**")

          st.write(
           f"⏱ **Duration:** {task.duration or 0} Minutes"
        )

          st.write(
           f"📅 **Scheduled Date:** {scheduled_date}"
         )

          st.write(
           f"🕒 **Time:** {start_time} → {end_time}"
         )

        deadline = (
        f"{task.due_date} {task.due_time}"
        if task.due_time
        else str(task.due_date)
       )

        st.write(
         f"🎯 **Deadline:** {deadline}"
      )

        st.write(
        f"📌 **Status:** {status}"
       )

    finally:

        db.close()