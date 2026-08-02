import streamlit as st

from modules.database.database import SessionLocal
from modules.calendar.calendar_service import get_today_schedule


def render_calendar():

    st.title("📅 Today's Calendar")

    db = SessionLocal()

    fixed, tasks = get_today_schedule(db)

    st.subheader("🏫 Fixed Timetable")

    if not fixed:
        st.info("No classes today.")

    else:

        for event in fixed:

            st.success(
                f"{event.start_time.strftime('%H:%M')} - "
                f"{event.end_time.strftime('%H:%M')} | "
                f"{event.title}"
            )

    st.divider()

    st.subheader("🤖 AI Scheduled Tasks")

    if not tasks:

        st.warning("No scheduled tasks.")

    else:

        for task in tasks:

            st.info(
                f"{task.scheduled_start.strftime('%H:%M')} - "
                f"{task.scheduled_end.strftime('%H:%M')} | "
                f"{task.title}"
            )

    db.close()