import streamlit as st
import pandas as pd

from modules.database.database import SessionLocal
from modules.database.crud import get_tasks


def render_analytics():

    st.title("📊 Analytics")

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
        # No Data
        # =====================================================

        if not tasks:

            st.info(
                "📭 No task data available yet."
            )

            st.write(
                "Create some tasks to see your productivity analytics."
            )

            return

        # =====================================================
        # Basic Statistics
        # =====================================================

        total = len(tasks)

        completed = len(
            [
                task
                for task in tasks
                if task.status == "Completed"
            ]
        )

        pending = len(
            [
                task
                for task in tasks
                if task.status == "Pending"
            ]
        )

        productivity = (
            round((completed / total) * 100)
            if total > 0
            else 0
        )

        # =====================================================
        # Statistics Cards
        # =====================================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "📋 Total Tasks",
                total
            )

        with c2:

            st.metric(
                "⏳ Pending",
                pending
            )

        with c3:

            st.metric(
                "✅ Completed",
                completed
            )

        with c4:

            st.metric(
                "⚡ Productivity",
                f"{productivity}%"
            )

        st.divider()

        # =====================================================
        # Completion Chart
        # =====================================================

        st.subheader("📈 Task Completion")

        chart_data = pd.DataFrame(
            {
                "Status": [
                    "Completed",
                    "Pending"
                ],
                "Tasks": [
                    completed,
                    pending
                ],
            }
        )

        st.bar_chart(
            chart_data.set_index("Status")
        )

        st.divider()

        # =====================================================
        # Priority Analysis
        # =====================================================

        st.subheader("🎯 Priority Analysis")

        high = len(
            [
                task
                for task in tasks
                if task.priority == "High"
            ]
        )

        medium = len(
            [
                task
                for task in tasks
                if task.priority == "Medium"
            ]
        )

        low = len(
            [
                task
                for task in tasks
                if task.priority == "Low"
            ]
        )

        priority_data = pd.DataFrame(
            {
                "Priority": [
                    "High",
                    "Medium",
                    "Low"
                ],
                "Tasks": [
                    high,
                    medium,
                    low
                ],
            }
        )

        st.bar_chart(
            priority_data.set_index("Priority")
        )

        st.divider()

        # =====================================================
        # Task Details
        # =====================================================

        st.subheader("📋 Your Tasks")

        task_rows = []

        for task in tasks:

            task_rows.append(
                {
                    "Task": task.title,
                    "Priority": task.priority,
                    "Status": task.status,
                    "Due Date": task.due_date,
                    "Due Time": task.due_time,
                    "Duration": (
                        f"{task.duration} min"
                        if task.duration
                        else "-"
                    ),
                }
            )

        df = pd.DataFrame(task_rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    finally:

        db.close()