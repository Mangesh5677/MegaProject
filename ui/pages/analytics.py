import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

from modules.database.database import SessionLocal
from modules.database.crud import get_tasks


def render_analytics():

    st.title("Analytics")

    user = st.session_state.user

    db = SessionLocal()

    try:

        tasks = get_tasks(db, user.id)

        if not tasks:
            st.info("📭 No task data available yet.")
            st.write("Create some tasks to see your productivity analytics.")
            return

        task_rows = []
        for task in tasks:
            due_date = task.due_date
            due_time = task.due_time.strftime("%I:%M %p") if task.due_time else "No time"
            task_rows.append(
                {
                    "Task": task.title,
                    "Priority": task.priority or "Low",
                    "Status": task.status,
                    "Due Date": due_date,
                    "Due Time": due_time,
                    "Duration": task.duration or 0,
                    "Due Date Value": pd.to_datetime(due_date) if due_date else pd.NaT,
                }
            )

        df = pd.DataFrame(task_rows)

        total = len(df)
        completed = len(df[df["Status"] == "Completed"])
        pending = len(df[df["Status"] == "Pending"])
        productivity = round((completed / total) * 100) if total else 0

        total_duration = int(df["Duration"].sum())
        avg_duration = int(round(df["Duration"].mean())) if not df.empty else 0

        upcoming = df[
            (df["Due Date Value"].notna()) &
            (df["Due Date Value"] >= pd.Timestamp(date.today())) &
            (df["Status"] == "Pending")
        ].sort_values("Due Date Value").head(5)

        upcoming = upcoming.copy()
        upcoming["Due Date"] = pd.to_datetime(upcoming["Due Date"], errors="coerce")

        high = len(df[df["Priority"] == "High"])
        medium = len(df[df["Priority"] == "Medium"])
        low = len(df[df["Priority"] == "Low"])

        if not df["Due Date Value"].dropna().empty:
            workload_trend = (
                df[df["Status"] == "Pending"]["Due Date Value"]
                .dt.floor("D")
                .value_counts()
                .sort_index()
                .reset_index()
            )
            workload_trend.columns = ["Date", "Pending Tasks"]
            workload_trend["Date"] = workload_trend["Date"].dt.strftime("%b %d")
        else:
            workload_trend = pd.DataFrame({"Date": ["No data"], "Pending Tasks": [0]})

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric("📋 Total Tasks", total)
        with c2:
            st.metric("✅ Completed", completed)
        with c3:
            st.metric("⏳ Pending", pending)
        with c4:
            st.metric("⚡ Productivity", f"{productivity}%")
        with c5:
            st.metric("🕒 Avg. Duration", f"{avg_duration} min")

        st.divider()

        st.subheader("📈 Productivity Overview")
        completion_chart = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Tasks": [completed, pending]
        })
        st.bar_chart(completion_chart.set_index("Status"))

        st.subheader("🎯 Priority Distribution")
        priority_data = pd.DataFrame({
            "Priority": ["High", "Medium", "Low"],
            "Tasks": [high, medium, low],
        })
        st.bar_chart(priority_data.set_index("Priority"))

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📅 Pending Workload Trend")
            if workload_trend.shape[0] == 1 and workload_trend.iloc[0]["Date"] == "No data":
                st.info("Add due dates to your tasks to see workload trend analysis.")
            else:
                st.line_chart(workload_trend.set_index("Date"), use_container_width=True)

        with col_right:
            st.subheader("🧠 Smart Insights")
            insights = []
            if pending > 0:
                insights.append(f"You still have {pending} pending tasks. Focus on the most urgent ones first.")
            if high > 0:
                insights.append(f"{high} high-priority tasks need faster follow-up to reduce backlog.")
            if productivity < 60:
                insights.append("Your completion rate is below the healthy range. Try batching similar tasks or reducing interruptions.")
            if productivity >= 70:
                insights.append("Strong momentum. Keep a consistent daily routine and protect your focus blocks.")
            if total_duration > 0:
                insights.append(f"Your total planned workload is {total_duration} minutes. Break it into focused work sessions.")

            if not insights:
                insights.append("No insights yet. Add tasks and track progress to unlock recommendations.")

            for insight in insights:
                st.write(f"• {insight}")

        st.divider()

        st.subheader("⏳ Upcoming Deadlines")
        if upcoming.empty:
            st.info("No upcoming pending deadlines found.")
        else:
            upcoming_display = upcoming[["Task", "Priority", "Due Date", "Due Time", "Duration"]].copy()
            upcoming_display["Due Date"] = pd.to_datetime(upcoming_display["Due Date"], errors="coerce").dt.strftime("%b %d, %Y")
            upcoming_display["Due Date"] = upcoming_display["Due Date"].fillna("No date")
            st.dataframe(upcoming_display, use_container_width=True, hide_index=True)

        st.divider()

        st.subheader("📋 Task Detail Summary")
        detail_df = df[["Task", "Priority", "Status", "Due Date", "Due Time", "Duration"]].copy()
        detail_df["Due Date"] = pd.to_datetime(detail_df["Due Date"], errors="coerce").dt.strftime("%b %d, %Y")
        detail_df["Due Date"] = detail_df["Due Date"].fillna("No date")
        detail_df["Duration"] = detail_df["Duration"].apply(lambda x: f"{int(x)} min" if pd.notna(x) else "0 min")
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

    finally:
        db.close()