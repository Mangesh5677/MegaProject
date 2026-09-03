import streamlit as st
from datetime import date, time

from modules.database.database import SessionLocal

from modules.database.crud import (
    add_task,
    get_tasks,
    delete_task,
    complete_task,
)


def render_tasks():

    st.title("My Tasks")

    st.caption(
        "Manage your personal tasks and deadlines."
    )

    # ============================================================
    # Logged-in user
    # ============================================================

    user = st.session_state.user

    db = SessionLocal()

    try:

        # ========================================================
        # ADD TASK
        # ========================================================

        with st.expander(
            "➕ Add New Task",
            expanded=True
        ):

            with st.form("add_task_form"):

                title = st.text_input(
                    "Task Title",
                    placeholder="Example: Complete LeetCode problems"
                )

                description = st.text_area(
                    "Description",
                    placeholder="Enter task details..."
                )

                col1, col2 = st.columns(2)

                with col1:

                    priority = st.selectbox(
                        "Priority",
                        [
                            "Low",
                            "Medium",
                            "High"
                        ]
                    )

                with col2:

                    duration = st.number_input(
                        "Duration (Minutes)",
                        min_value=15,
                        max_value=600,
                        value=60,
                        step=15
                    )

                task_type = st.selectbox(
                    "Task Type",
                    ["Once", "Daily / Running"],
                    help="Once = one-time task. Daily / Running = repeated task scheduled every day."
                )

                col3, col4 = st.columns(2)

                with col3:

                    due_date = st.date_input(
                        "Due Date",
                        value=date.today()
                    )

                with col4:

                    due_time = st.time_input(
                        "Due Time",
                        value=time(18, 0)
                    )

                email = st.text_input(
                    "Reminder Email",
                    value=user.email
                )

                submitted = st.form_submit_button(
                    "➕ Add Task",
                    use_container_width=True
                )

                if submitted:

                    if not title.strip():

                        st.error(
                            "❌ Please enter a task title."
                        )

                    else:

                        add_task(
                            db=db,
                            user_id=user.id,
                            title=title.strip(),
                            description=description.strip(),
                            priority=priority,
                            due_date=due_date,
                            due_time=due_time,
                            duration=duration,
                            email=email.strip(),
                            task_type=task_type,
                        )

                        st.success(
                            "✅ Task added successfully!"
                        )

                        st.rerun()

        st.divider()

        # ========================================================
        # GET ONLY LOGGED-IN USER'S TASKS
        # ========================================================

        tasks = get_tasks(
            db,
            user.id
        )

        st.subheader(
            f"📝 Your Tasks ({len(tasks)})"
        )

        # ========================================================
        # NO TASKS
        # ========================================================

        if not tasks:

            st.info(
                "🎉 You don't have any tasks yet. "
                "Add your first task above!"
            )

        # ========================================================
        # TASK LIST
        # ========================================================

        else:

            for task in tasks:

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

                # ------------------------------------------------
                # Task Card
                # ------------------------------------------------

                with st.container(border=True):

                    col1, col2 = st.columns(
                        [5, 1]
                    )

                    with col1:

                        st.markdown(
                            f"### 📌 {task.title}"
                        )

                        if task.description:

                            st.write(
                                task.description
                            )

                        st.write(
                            f"**Priority:** {badge}"
                        )

                        st.write(
                            f"**Task Type:** {task.task_type or 'Once'}"
                        )

                        st.write(
                            f"**Duration:** "
                            f"{task.duration or 0} minutes"
                        )

                        due_time_display = (
                            task.due_time.strftime("%I:%M %p")
                            if task.due_time
                            else "No time"
                        )

                        st.write(
                            f"**Deadline:** "
                            f"{task.due_date} "
                            f"at "
                            f"{due_time_display}"
                        )

                        st.write(
                            f"**Status:** {status}"
                        )

                        if task.scheduled_date:

                            scheduled_start_display = (
                                task.scheduled_start.strftime("%I:%M %p")
                                if task.scheduled_start
                                else "--:--"
                            )
                            scheduled_end_display = (
                                task.scheduled_end.strftime("%I:%M %p")
                                if task.scheduled_end
                                else "--:--"
                            )

                            st.write(
                                f"🤖 **AI Scheduled:** "
                                f"{task.scheduled_date} "
                                f"{scheduled_start_display} "
                                f"→ "
                                f"{scheduled_end_display}"
                            )

                    with col2:

                        # ------------------------------------------------
                        # Complete / Reopen
                        # ------------------------------------------------

                        if task.status == "Pending":

                            if st.button(
                                "✅ Complete",
                                key=f"complete_{task.id}",
                                use_container_width=True,
                            ):

                                complete_task(
                                    db,
                                    user.id,
                                    task.id
                                )

                                st.success(
                                    "Task completed!"
                                )

                                st.rerun()

                        else:

                            st.success(
                                "Completed"
                            )

                        # ------------------------------------------------
                        # Delete
                        # ------------------------------------------------

                        if st.button(
                            "🗑 Delete",
                            key=f"delete_{task.id}",
                            use_container_width=True,
                        ):

                            deleted = delete_task(
                                db,
                                user.id,
                                task.id
                            )

                            if deleted:

                                st.success(
                                    "Task deleted successfully."
                                )

                            else:

                                st.error(
                                    "Task not found."
                                )

                            st.rerun()

    finally:

        db.close()