import streamlit as st

from modules.database.database import SessionLocal
from modules.scheduler.scheduler import generate_schedule


def render_ai_scheduler():

    st.title("🤖 AI Scheduler")

    db = SessionLocal()

    if st.button("🧠 Generate Schedule"):

        result = generate_schedule(db)

        if isinstance(result, str):
            st.warning(result)
        else:
            st.success("Schedule Generated!")

            for task in result:
                st.write(f"📌 {task['task']}")
                st.write(f"⏱ {task['duration']} min")
                st.write(f"✅ {task['status']}")
                st.divider()

    db.close()