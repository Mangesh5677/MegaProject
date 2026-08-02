import streamlit as st

from modules.database.database import SessionLocal
from modules.database.crud import (
    get_tasks,
    get_fixed_schedules,
)
from modules.advisor.groq_advisor import get_ai_advice


def render_ai_advisor():

    st.title("🤖 AI Study Advisor")

    db = SessionLocal()

    if st.button("✨ Get AI Advice"):

        tasks = get_tasks(db)
        timetable = get_fixed_schedules(db)

        task_text = "\n".join(
            [
                f"{t.title} | {t.priority} | Due: {t.due_date}"
                for t in tasks
            ]
        )

        timetable_text = "\n".join(
            [
                f"{x.day} {x.start_time}-{x.end_time} {x.title}"
                for x in timetable
            ]
        )

        advice = get_ai_advice(
            task_text,
            timetable_text
        )

        st.success(advice)

    db.close()