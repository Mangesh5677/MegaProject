import streamlit as st
from modules.database.database import SessionLocal
from modules.database.crud import get_fixed_schedules, get_tasks

def render_calendar():
    st.title("📅 Calendar")

    db = SessionLocal()

    st.subheader("Fixed Timetable")

    schedules = get_fixed_schedules(db)

    if schedules:
        for item in schedules:
            st.write(
                f"**{item.day}** | "
                f"{item.start_time} - {item.end_time} | "
                f"{item.title}"
            )
    else:
        st.info("No timetable added.")

    st.divider()

    st.subheader("Tasks")

    tasks = get_tasks(db)

    if tasks:
        for task in tasks:
            st.write(
                f"📋 {task.title} | "
                f"Status: {task.status}"
            )
    else:
        st.info("No tasks found.")

    db.close()