import streamlit as st

from modules.database.database import SessionLocal
from modules.database.crud import get_tasks
from modules.ai.scheduler import generate_schedule


def render_ai_scheduler():

    st.title("🤖 AI Smart Scheduler")

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
                use_container_width=True
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

                    with st.expander("View Unscheduled Tasks"):

                        for task in unscheduled:
                            st.write(f"• {task.title}")

                st.rerun()

        with col2:

            if st.button(
                "🔄 Refresh",
                use_container_width=True
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

        # ==========================================================
        # GET SCHEDULED TASKS
        # ==========================================================

        scheduled_tasks = [
            task
            for task in tasks
            if (
                task.scheduled_date is not None
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

        st.subheader("📅 Your AI Schedule")

        if not scheduled_tasks:

            st.info(
                "No tasks are currently scheduled."
            )

            st.write(
                "Click **🚀 Generate AI Schedule** to create your schedule."
            )

            return

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
            use_container_width=True,
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

    finally:

        # ==========================================================
        # CLOSE DATABASE
        # ==========================================================

        db.close()