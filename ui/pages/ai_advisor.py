import streamlit as st

from modules.database.database import SessionLocal
from modules.database.crud import (
    get_tasks,
    get_fixed_schedules,
)
from modules.advisor.groq_advisor import get_ai_advice


def render_ai_advisor():

    st.title("🤖 AI Study Advisor")

    st.caption(
        "Get personalized study advice based on your tasks and timetable."
    )

    user = st.session_state.user

    db = SessionLocal()

    try:

        if st.button(
            "✨ Get AI Advice",
            use_container_width=True
        ):

            # ==================================================
            # Get ONLY current user's data
            # ==================================================

            tasks = get_tasks(
                db,
                user.id
            )

            timetable = get_fixed_schedules(
                db,
                user.id
            )

            # ==================================================
            # Check if user has data
            # ==================================================

            if not tasks and not timetable:

                st.info(
                    "📭 You don't have any tasks or timetable entries yet."
                )

                return

            # ==================================================
            # Prepare Task Data
            # ==================================================

            if tasks:

                task_text = "\n".join(
                    [
                        (
                            f"Task: {task.title} | "
                            f"Priority: {task.priority} | "
                            f"Status: {task.status} | "
                            f"Due: {task.due_date} {task.due_time} | "
                            f"Duration: {task.duration} minutes"
                        )
                        for task in tasks
                    ]
                )

            else:

                task_text = "No tasks available."

            # ==================================================
            # Prepare Timetable Data
            # ==================================================

            if timetable:

                timetable_text = "\n".join(
                    [
                        (
                            f"{item.day} | "
                            f"{item.start_time} - "
                            f"{item.end_time} | "
                            f"{item.title} | "
                            f"{item.category}"
                        )
                        for item in timetable
                    ]
                )

            else:

                timetable_text = "No fixed timetable available."

            # ==================================================
            # Generate AI Advice
            # ==================================================

            with st.spinner(
                "🤖 AI is analyzing your productivity..."
            ):

                advice = get_ai_advice(
                    task_text,
                    timetable_text
                )

            # ==================================================
            # Display Advice
            # ==================================================

            st.subheader("💡 Your Personalized Advice")

            st.success(advice)

    finally:

        db.close()