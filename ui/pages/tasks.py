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

    st.title("📋 Task Manager")
    st.caption("Manage your daily tasks efficiently.")

    db = SessionLocal()

    # ==================================================
    # Add Task
    # ==================================================

    with st.expander("➕ Add New Task", expanded=True):

        with st.form("task_form"):

            title = st.text_input(
                "📝 Task Title"
            )

            description = st.text_area(
                "📄 Description",
                height=100
            )

            email = st.text_input(
                "📧 Reminder Email",
                placeholder="example@gmail.com"
            )

            priority = st.selectbox(
                "⭐ Priority",
                [
                    "High",
                    "Medium",
                    "Low"
                ]
            )

            duration = st.number_input(
                "⏱ Duration (Minutes)",
                min_value=15,
                max_value=600,
                value=60,
                step=15
            )

            due_date = st.date_input(
                "📅 Deadline Date",
                value=date.today()
            )

            due_time = st.time_input(
                "🕒 Deadline Time",
                value=time(18, 0)
            )

            submitted = st.form_submit_button(
                "🚀 Add Task"
            )

            if submitted:

                if title.strip() == "":
                    st.error("Task title is required.")

                else:

                    add_task(
                        db,
                        st.session_state.user.id,
                        title,
                        description,
                        priority,
                        due_date,
                        due_time,
                        duration,
                        email
                    )

                    st.success("✅ Task Added Successfully")

                    st.rerun()

    st.divider()

    # ==================================================
    # Show Tasks
    # ==================================================

    st.subheader("📋 All Tasks")

    tasks = get_tasks(
    db,
    st.session_state.user.id
)

    if len(tasks) == 0:

        st.info("No Tasks Found.")

    else:

        for task in tasks:

            if task.priority == "High":
                border = "#ef4444"
                badge = "🔴 HIGH"

            elif task.priority == "Medium":
                border = "#f59e0b"
                badge = "🟡 MEDIUM"

            else:
                border = "#22c55e"
                badge = "🟢 LOW"

            status = (
                "✅ Completed"
                if task.status == "Completed"
                else "⏳ Pending"
            )

            st.markdown(
                f"""
<div style="
background:#1e293b;
padding:22px;
border-radius:20px;
border-left:8px solid {border};
margin-bottom:20px;
box-shadow:0 10px 20px rgba(0,0,0,.25);
">

<h2 style="color:white;">
📌 {task.title}
</h2>

<p style="color:#d1d5db;font-size:16px;">
{task.description}
</p>

<hr>

<p style="font-size:18px;">
<b>{badge}</b>
</p>

<p>
⏱ <b>Duration:</b> {task.duration} Minutes
</p>

<p>
📅 <b>Deadline:</b> {task.due_date}
</p>

<p>
🕒 <b>Time:</b> {task.due_time}
</p>

<p>
📧 <b>Email:</b> {task.email}
</p>

<p>
📌 <b>Status:</b> {status}
</p>

</div>
""",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:

                if task.status != "Completed":

                    if st.button(
                        "✅ Complete",
                        key=f"complete_{task.id}"
                    ):

                        complete_task(
                            db,
                            task.id
                        )

                        st.success("Task Completed")

                        st.rerun()

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{task.id}"
                ):

                    delete_task(
                    db,
                    st.session_state.user.id,
                    task.id
                    )

                    st.success("✅ Task deleted successfully.")

                    st.rerun()

    db.close()