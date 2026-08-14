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
        "Get personalized study advice based only on your data."
    )

    db = SessionLocal()

    try:
        user_id = st.session_state.user.id

        if st.button("✨ Get AI Advice"):

            # ==========================================
            # Get ONLY logged-in user's data
            # ==========================================

            tasks = get_tasks(
                db,
                user_id
            )

            timetable = get_fixed_schedules(
                db,
                user_id
            )

            # ==========================================
            # Prepare Task Information
            # ==========================================

            if tasks:

                task_text = "\n".join(
                    [
                        (
                            f"Task: {task.title} | "
                            f"Priority: {task.priority} | "
                            f"Status: {task.status} | "
                            f"Due: {task.due_date} {task.due_time}"
                        )
                        for task in tasks
                    ]
                )

            else:

                task_text = "No tasks added yet."

            # ==========================================
            # Prepare Timetable Information
            # ==========================================

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

                timetable_text = "No fixed timetable added yet."

            # ==========================================
            # Get AI Advice
            # ==========================================

            with st.spinner("🤖 AI is analyzing your schedule..."):

                advice = get_ai_advice(
                    task_text,
                    timetable_text
                )

            st.subheader("💡 Your Personalized Advice")

            st.success(advice)

    except Exception as e:

        st.error(
            f"❌ Unable to generate AI advice: {e}"
        )

    finally:

        db.close()