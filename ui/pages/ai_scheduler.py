from datetime import date, time

import streamlit as st

from modules.database.database import SessionLocal
from modules.database.crud import get_tasks
from modules.database.models import FixedSchedule, Task
from modules.ai.scheduler import generate_schedule
from modules.analytics.activity_service import log_activity


def render_ai_scheduler():

    st.title("AI Smart Scheduler")

    st.markdown(
        """
        The AI Scheduler automatically plans your pending tasks based on:

        - 🎓 Fixed College Timetable
        - ⭐ Task Priority
        - 📅 Deadline
        - ⏱️ Task Duration
        """
    )

    user = st.session_state.user
    db = SessionLocal()

    try:

        # ==========================================================
        # GENERATE / REFRESH BUTTONS
        # ==========================================================

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🚀 Generate AI Schedule",
                width="stretch"
            ):

                scheduled, unscheduled = generate_schedule(
                    db,
                    user.id
                )
                log_activity(
                    db,
                    user.id,
                    "AI_SCHEDULER",
                    "User generated an AI schedule"
                )

                st.success(
                    f"✅ {len(scheduled)} task(s) scheduled successfully."
                )

                if unscheduled:

                    st.warning(
                        f"⚠️ {len(unscheduled)} task(s) could not be scheduled."
                    )

                    with st.expander("View Unscheduled Tasks"):

                        for task in unscheduled:
                            st.write(f"• {task.title}")

        with col2:

            if st.button(
                "🔄 Refresh",
                width="stretch"
            ):
                st.rerun()

        st.divider()

        # ==========================================================
        # GET ALL USER TASKS
        # ==========================================================

        tasks = get_tasks(
            db,
            user.id
        )
        today = date.today()

        # ==========================================================
        # GET TODAY'S AI-SCHEDULED TASKS
        # ==========================================================

        scheduled_tasks = [
            task
            for task in tasks
            if (
                task.status != "Completed"
                and
                task.scheduled_date == today
                and task.scheduled_start is not None
                and task.scheduled_end is not None
            )
        ]

        # ==========================================================
        # SORT TASKS
        # ==========================================================

        scheduled_tasks.sort(
            key=lambda task: (
                task.scheduled_date,
                task.scheduled_start
            )
        )

        # ==========================================================
        # PAGE HEADER
        # ==========================================================

        st.subheader("AI-Generated Tasks for Today")

        if not scheduled_tasks:

            st.info(
                "No AI-generated tasks are scheduled for today."
            )

            st.write(
                "Click **🚀 Generate AI Schedule** to create today's schedule."
            )

        else:

            # ==========================================================
            # SUMMARY
            # ==========================================================

            st.success(
                f"📌 {len(scheduled_tasks)} task(s) currently scheduled."
            )

            # ==========================================================
            # TABLE VIEW
            # ==========================================================

            st.markdown("### 📊 Schedule Overview")

            table_data = []

            for task in scheduled_tasks:

                if task.status == "Completed":
                    status = "✅ Completed"
                else:
                    status = "⏳ Pending"

                table_data.append(
                    {
                        "Task": task.title,
                        "Priority": task.priority,
                        "Date": str(task.scheduled_date),
                        "Start": task.scheduled_start.strftime("%I:%M %p"),
                        "End": task.scheduled_end.strftime("%I:%M %p"),
                        "Duration": f"{task.duration} min",
                        "Deadline": (
                            str(task.due_date)
                            if task.due_date
                            else "No Deadline"
                        ),
                        "Status": status,
                    }
                )

            st.dataframe(
                table_data,
                width="stretch",
                hide_index=True
            )

            st.divider()

            # ==========================================================
            # CARD VIEW
            # ==========================================================

            st.markdown("### 🗓️ Scheduled Tasks")

        for task in scheduled_tasks:

            # ------------------------------------------------------
            # PRIORITY
            # ------------------------------------------------------

            priority = str(
                task.priority or "Low"
            ).strip().lower()

            if priority == "high":

                priority_badge = "🔴 HIGH"

            elif priority == "medium":

                priority_badge = "🟡 MEDIUM"

            else:

                priority_badge = "🟢 LOW"

            # ------------------------------------------------------
            # STATUS
            # ------------------------------------------------------

            if task.status == "Completed":

                status = "✅ Completed"

            else:

                status = "⏳ Pending"

            # ------------------------------------------------------
            # TASK INFORMATION
            # ------------------------------------------------------

            title = task.title or "Untitled Task"

            description = (
                task.description
                or "No Description"
            )

            duration = (
                task.duration
                or 0
            )

            scheduled_date = (
                task.scheduled_date
            )

            scheduled_start = (
                task.scheduled_start.strftime("%I:%M %p")
            )

            scheduled_end = (
                task.scheduled_end.strftime("%I:%M %p")
            )

            due_date = (
                task.due_date
                if task.due_date
                else "No Deadline"
            )

            # ======================================================
            # CARD
            # ======================================================

            with st.container(border=True):

                # TITLE

                st.markdown(
                    f"## 📌 {title}"
                )

                # DESCRIPTION

                st.write(
                    description
                )

                st.divider()

                # FIRST ROW

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.markdown(
                        f"""
                        **⭐ Priority**

                        {priority_badge}
                        """
                    )

                with col2:

                    st.markdown(
                        f"""
                        **⏱️ Duration**

                        {duration} Minutes
                        """
                    )

                with col3:

                    st.markdown(
                        f"""
                        **📌 Status**

                        {status}
                        """
                    )

                # SPACE

                st.write("")

                # SECOND ROW

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.markdown(
                        f"""
                        **📅 Scheduled Date**

                        {scheduled_date}
                        """
                    )

                with col2:

                    st.markdown(
                        f"""
                        **🕒 Scheduled Time**

                        {scheduled_start} → {scheduled_end}
                        """
                    )

                with col3:

                    st.markdown(
                        f"""
                        **🎯 Deadline**

                        {due_date}
                        """
                    )

        # ==========================================================
        # TODAY'S FULL TIMETABLE
        # ==========================================================

        st.divider()
        st.subheader("📅 Today's Timetable")

        today_day = today.strftime("%A")

        fixed_events = (
            db.query(FixedSchedule)
            .filter(
                FixedSchedule.user_id == user.id,
                FixedSchedule.day == today_day,
            )
            .all()
        )

        today_tasks = (
            db.query(Task)
            .filter(
                Task.user_id == user.id,
                Task.scheduled_date == today,
                Task.scheduled_start.isnot(None),
                Task.scheduled_end.isnot(None),
            )
            .all()
        )

        timetable_entries = [
            (
                event.start_time,
                event.end_time,
                event.title,
                event.category or "Fixed event",
                "Fixed",
            )
            for event in fixed_events
        ]

        timetable_entries.extend(
            (
                task.scheduled_start,
                task.scheduled_end,
                task.title,
                f"{task.priority or 'Low'} priority · {task.duration or 0} min",
                task.status,
            )
            for task in today_tasks
        )
        timetable_entries.sort(
            key=lambda entry: (entry[0] or time.min, entry[1] or time.min)
        )

        if not timetable_entries:
            st.info("No fixed events or AI-scheduled tasks for today.")
        else:
            today_timetable = [
                {
                    "Start": (
                        start.strftime("%I:%M %p")
                        if start
                        else "--:--"
                    ),
                    "End": (
                        end.strftime("%I:%M %p")
                        if end
                        else "--:--"
                    ),
                    "Activity": title,
                    "Type": category,
                    "Status": status,
                }
                for start, end, title, category, status in timetable_entries
            ]

            st.dataframe(
                today_timetable,
                width="stretch",
                hide_index=True,
            )

    finally:

        # ==========================================================
        # CLOSE DATABASE
        # ==========================================================

        db.close()