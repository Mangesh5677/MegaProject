import streamlit as st
import plotly.express as px

from modules.database.database import SessionLocal
from modules.analytics.analytics_service import (
    get_statistics,
    get_recent_tasks,
)


def render_analytics():

    st.title("📊 Analytics Dashboard")

    db = SessionLocal()

    stats = get_statistics(db)

    # ==========================
    # Top Metrics
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📋 Total", stats["total"])
    col2.metric("✅ Completed", stats["completed"])
    col3.metric("⏳ Pending", stats["pending"])
    col4.metric("⚡ Productivity", f"{stats['productivity']}%")

    st.divider()

    # ==========================
    # Charts
    # ==========================

    left, right = st.columns(2)

    with left:

        labels = []
        values = []

        for k, v in stats["priority"].items():

            if v > 0:
                labels.append(k)
                values.append(v)

        if values:

            fig = px.pie(
                names=labels,
                values=values,
                title="Priority Distribution",
                hole=0.45,
            )

            fig.update_layout(
                template="plotly_dark",
                height=450,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info("No priority data available.")

    with right:

        fig = px.bar(
            x=["Completed", "Pending"],
            y=[
                stats["completed"],
                stats["pending"],
            ],
            text=[
                stats["completed"],
                stats["pending"],
            ],
            title="Task Status",
        )

        fig.update_layout(
            template="plotly_dark",
            height=450,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.divider()

    # ==========================
    # Productivity
    # ==========================

    st.subheader("📈 Productivity")

    st.progress(stats["productivity"] / 100)

    st.write(f"### {stats['productivity']}% Completed")

    if stats["productivity"] >= 90:
        st.success("🏆 Excellent Productivity")

    elif stats["productivity"] >= 70:
        st.info("🚀 Great Progress")

    elif stats["productivity"] >= 50:
        st.warning("🙂 Keep Going")

    else:
        st.error("⚠ You have many pending tasks.")

    st.divider()

    # ==========================
    # Recent Tasks
    # ==========================

    st.subheader("📋 Recent Tasks")

    tasks = get_recent_tasks(db)

    if tasks:

        table = []

        for task in tasks:

            table.append(
                {
                    "Title": task.title,
                    "Priority": task.priority,
                    "Status": task.status,
                    "Deadline": task.due_date,
                    "Duration (min)": task.duration,
                    "Scheduled": (
                        f"{task.scheduled_start} - {task.scheduled_end}"
                        if task.scheduled_start
                        else "Not Scheduled"
                    ),
                }
            )

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No tasks available.")

    db.close()