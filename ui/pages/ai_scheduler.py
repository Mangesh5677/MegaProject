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

    try:

        # ==========================================
        # Logged-in User
        # ==========================================

        user_id = st.session_state.user.id

        col1, col2 = st.columns([1, 1])

        # ==========================================
        # Generate AI Schedule
        # ==========================================

        with col1:

            if st.button(
                "🚀 Generate AI Schedule",
                use_container_width=True
            ):

                with st.spinner(
                    "🤖 AI is generating your schedule..."
                ):

                    scheduled, unscheduled = generate_schedule(
                        db,
                        user_id
                    )

                st.success(
                    f"✅ {len(scheduled)} task(s) scheduled successfully."
                )

                if unscheduled:

                    st.warning(
                        f"⚠ {len(unscheduled)} task(s) could not be scheduled."
                    )

                    with st.expander(
                        "View Unscheduled Tasks"
                    ):

                        for task in unscheduled:

                            st.write(
                                f"• {task.title}"
                            )

        # ==========================================
        # Refresh
        # ==========================================

        with col2:

            if st.button(
                "🔄 Refresh",
                use_container_width=True
            ):

                st.rerun()

        st.divider()

        # ==========================================
        # Today's AI Schedule
        # ==========================================

        st.subheader(
            "📅 Today's AI Schedule"
        )

        # IMPORTANT:
        # Only get tasks belonging to logged-in user

        tasks = get_tasks(
            db,
            user_id
        )

        scheduled_tasks = [
            task
            for task in tasks
            if task.scheduled_start is not None
        ]

        # ==========================================
        # No Schedule
        # ==========================================

        if not scheduled_tasks:

            st.info(
                "No tasks scheduled.\n\n"
                "Click **Generate AI Schedule**."
            )

        # ==========================================
        # Display Schedule
        # ==========================================

        else:

            scheduled_tasks.sort(
                key=lambda x: (
                    x.scheduled_date or x.due_date,
                    x.scheduled_start
                )
            )

            for task in scheduled_tasks:

                # ------------------------------
                # Priority
                # ------------------------------

                if task.priority == "High":

                    color = "#ef4444"
                    badge = "🔴 HIGH"

                elif task.priority == "Medium":

                    color = "#f59e0b"
                    badge = "🟡 MEDIUM"

                else:

                    color = "#22c55e"
                    badge = "🟢 LOW"

                # ------------------------------
                # Status
                # ------------------------------

                if task.status == "Completed":

                    status = "✅ Completed"

                else:

                    status = "⏳ Pending"

                # ------------------------------
                # Safe Date / Time
                # ------------------------------

                scheduled_date = (
                    task.scheduled_date
                    if task.scheduled_date
                    else "Not Scheduled"
                )

                if task.scheduled_start:

                    start_time = task.scheduled_start.strftime(
                        "%H:%M"
                    )

                else:

                    start_time = "--:--"

                if task.scheduled_end:

                    end_time = task.scheduled_end.strftime(
                        "%H:%M"
                    )

                else:

                    end_time = "--:--"

                # ------------------------------
                # Task Card
                # ------------------------------

                st.markdown(
                    f"""
<div class="task-card"
     style="border-left:8px solid {color};">

<h3>📌 {task.title}</h3>

<p>
{task.description or "No Description"}
</p>

<hr>

<b>{badge}</b>

<br><br>

⏱ Duration:
<b>{task.duration or 0} Minutes</b>

<br>

📅 Scheduled Date:
<b>{scheduled_date}</b>

<br>

🕒 Time:
<b>
{start_time}
 →
{end_time}
</b>

<br>

🎯 Deadline:
<b>
{task.due_date or "No Deadline"}
</b>

<br>

📌 Status:
<b>
{status}
</b>

</div>
""",
                    unsafe_allow_html=True
                )

    except Exception as e:

        st.error(
            f"❌ AI Scheduler Error: {e}"
        )

    finally:

        db.close()