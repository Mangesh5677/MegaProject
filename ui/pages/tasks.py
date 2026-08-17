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

    st.title("📝 Task Manager")
    st.caption("Create, manage, complete and delete your tasks.")

    # =========================================================
    # Logged-in User
    # =========================================================

    user = st.session_state.user

    # Supports SQLAlchemy user object
    # and dictionary-based user session
    if hasattr(user, "id"):
        user_id = user.id
    elif isinstance(user, dict):
        user_id = user.get("id")
    else:
        st.error("Unable to identify logged-in user.")
        return

    # =========================================================
    # Database
    # =========================================================

    db = SessionLocal()

    try:

        # =====================================================
        # Add New Task
        # =====================================================

        st.subheader("➕ Add New Task")

        with st.form("add_task_form", clear_on_submit=True):

            title = st.text_input(
                "Task Title",
                placeholder="Enter task title"
            )

            description = st.text_area(
                "Description",
                placeholder="Enter task description"
            )

            col1, col2 = st.columns(2)

            with col1:

                priority = st.selectbox(
                    "Priority",
                    [
                        "Low",
                        "Medium",
                        "High"
                    ],
                    index=1
                )

                duration = st.number_input(
                    "Duration (minutes)",
                    min_value=15,
                    max_value=600,
                    value=60,
                    step=15
                )

            with col2:

                due_date = st.date_input(
                    "Due Date",
                    value=date.today()
                )

                due_time = st.time_input(
                    "Due Time",
                    value=time(18, 0)
                )

            email = st.text_input(
                "Reminder Email",
                placeholder="Enter email for reminders"
            )

            submitted = st.form_submit_button(
                "➕ Add Task",
                use_container_width=True
            )

            if submitted:

                if not title.strip():

                    st.error("Please enter a task title.")

                else:

                    try:

                        add_task(
                            db=db,
                            user_id=user_id,
                            title=title.strip(),
                            description=description.strip(),
                            priority=priority,
                            due_date=due_date,
                            due_time=due_time,
                            duration=duration,
                            email=email.strip()
                        )

                        st.success(
                            "✅ Task added successfully!"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Failed to add task: {e}"
                        )

        st.divider()

        # =====================================================
        # Get Current User's Tasks
        # =====================================================

        tasks = get_tasks(
            db,
            user_id
        )

        # =====================================================
        # Task Statistics
        # =====================================================

        total_tasks = len(tasks)

        completed_tasks = sum(
            1
            for task in tasks
            if task.status == "Completed"
        )

        pending_tasks = sum(
            1
            for task in tasks
            if task.status != "Completed"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📋 Total Tasks",
                total_tasks
            )

        with col2:
            st.metric(
                "⏳ Pending",
                pending_tasks
            )

        with col3:
            st.metric(
                "✅ Completed",
                completed_tasks
            )

        st.divider()

        # =====================================================
        # Task List
        # =====================================================

        st.subheader("📋 My Tasks")

        if not tasks:

            st.info(
                "No tasks found. Add your first task above."
            )

            return

        # =====================================================
        # Display Tasks
        # =====================================================

        for task in tasks:

            is_completed = task.status == "Completed"

            # -------------------------------------------------
            # Task Container
            # -------------------------------------------------

            with st.container(border=True):

                # =================================================
                # Header
                # =================================================

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    if is_completed:

                        st.markdown(
                            f"### ✅ ~~{task.title}~~"
                        )

                    else:

                        st.markdown(
                            f"### 📝 {task.title}"
                        )

                with col2:

                    if task.priority == "High":

                        st.error(
                            "🔴 High"
                        )

                    elif task.priority == "Medium":

                        st.warning(
                            "🟡 Medium"
                        )

                    else:

                        st.info(
                            "🟢 Low"
                        )

                # =================================================
                # Description
                # =================================================

                if task.description:

                    st.write(
                        task.description
                    )

                # =================================================
                # Task Information
                # =================================================

                info_col1, info_col2, info_col3 = st.columns(3)

                with info_col1:

                    if task.due_date:

                        st.caption(
                            f"📅 Due Date: {task.due_date}"
                        )

                with info_col2:

                    if task.due_time:

                        st.caption(
                            f"⏰ Due Time: {task.due_time}"
                        )

                with info_col3:

                    if task.duration:

                        st.caption(
                            f"⏱️ Duration: {task.duration} min"
                        )

                # =================================================
                # Status
                # =================================================

                if is_completed:

                    st.success(
                        "Status: Completed"
                    )

                else:

                    st.warning(
                        "Status: Pending"
                    )

                # =================================================
                # Buttons
                # =================================================

                button_col1, button_col2 = st.columns(2)

                # -------------------------------------------------
                # Complete Button
                # -------------------------------------------------

                with button_col1:

                    if not is_completed:

                        if st.button(
                            "✅ Complete",
                            key=f"complete_{task.id}",
                            use_container_width=True
                        ):

                            try:

                                result = complete_task(
                                    db,
                                    user_id,
                                    task.id
                                )

                                if result:

                                    st.success(
                                        "✅ Task completed successfully!"
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        "Task not found."
                                    )

                            except Exception as e:

                                st.error(
                                    f"Failed to complete task: {e}"
                                )

                    else:

                        st.button(
                            "✅ Completed",
                            key=f"completed_{task.id}",
                            disabled=True,
                            use_container_width=True
                        )

                # -------------------------------------------------
                # Delete Button
                # -------------------------------------------------

                with button_col2:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{task.id}",
                        use_container_width=True
                    ):

                        try:

                            delete_task(
                                db,
                                user_id,
                                task.id
                            )

                            st.success(
                                "🗑️ Task deleted successfully!"
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Failed to delete task: {e}"
                            )

    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )

    finally:

        db.close()