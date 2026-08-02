import streamlit as st

from modules.database.database import SessionLocal
from modules.ai.scheduler import generate_schedule
from modules.database.crud import get_tasks


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

    db = SessionLocal()

    col1, col2 = st.columns([1, 1])

    with col1:

        if st.button("🚀 Generate AI Schedule", use_container_width=True):

            scheduled, unscheduled = generate_schedule(db)

            st.success(
                f"✅ {len(scheduled)} task(s) scheduled successfully."
            )

            if unscheduled:

                st.warning(
                    f"⚠ {len(unscheduled)} task(s) could not be scheduled."
                )

                with st.expander("View Unscheduled Tasks"):

                    for task in unscheduled:
                        st.write(f"• {task.title}")

    with col2:

        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    st.divider()

    st.subheader("📅 Today's AI Schedule")

    tasks = get_tasks(db)

    scheduled_tasks = [
        t for t in tasks
        if t.scheduled_start is not None
    ]

    if not scheduled_tasks:

        st.info(
            "No tasks scheduled.\n\nClick **Generate AI Schedule**."
        )

    else:

        scheduled_tasks.sort(
            key=lambda x: x.scheduled_start
        )

        for task in scheduled_tasks:

            if task.priority == "High":
                color = "#ef4444"
                badge = "🔴 HIGH"

            elif task.priority == "Medium":
                color = "#f59e0b"
                badge = "🟡 MEDIUM"

            else:
                color = "#22c55e"
                badge = "🟢 LOW"

            status = (
                "✅ Completed"
                if task.status == "Completed"
                else "⏳ Pending"
            )

            st.markdown(
                f"""
<div class="task-card" style="border-left:8px solid {color};">

<h3>📌 {task.title}</h3>

<p>{task.description or "No Description"}</p>

<hr>

<b>{badge}</b>

<br><br>

⏱ Duration : <b>{task.duration} Minutes</b>

<br>

📅 Scheduled Date : <b>{task.scheduled_date}</b>

<br>

🕒 Time :
<b>
{task.scheduled_start.strftime("%H:%M")}
 →
{task.scheduled_end.strftime("%H:%M")}
</b>

<br>

🎯 Deadline :
<b>{task.due_date}</b>

<br>

📌 Status :
<b>{status}</b>

</div>
""",
                unsafe_allow_html=True,
            )

    db.close()