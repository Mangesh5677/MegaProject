import streamlit as st
from datetime import time

from modules.database.database import SessionLocal
from modules.database.crud import (
    add_fixed_schedule,
    get_fixed_schedules,
    delete_fixed_schedule
)


def render_fixed_schedule():

    st.title("📅 Fixed Weekly Timetable")

    db = SessionLocal()

    with st.form("schedule"):

        day = st.selectbox(
            "Day",
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ]
        )

        title = st.text_input("Subject / Event")

        category = st.selectbox(
            "Category",
            [
                "College",
                "Study",
                "Gym",
                "Travel",
                "Lunch",
                "Sleep",
                "Other"
            ]
        )

        start = st.time_input(
            "Start Time",
            value=time(9, 0)
        )

        end = st.time_input(
            "End Time",
            value=time(10, 0)
        )

        if st.form_submit_button("Save"):
            add_fixed_schedule(
                db,
                day,
                title,
                category,
                start,
                end
            )
            st.success("Timetable Saved")
            st.rerun()

    st.divider()

    st.subheader("Weekly Timetable")

    schedules = get_fixed_schedules(db)

    for item in schedules:

        col1, col2 = st.columns([6, 1])

        with col1:
            st.write(
                f"**{item.day}** | "
                f"{item.start_time} - {item.end_time} | "
                f"{item.title} ({item.category})"
            )

        with col2:
            if st.button("Delete", key=item.id):
                delete_fixed_schedule(db, item.id)
                st.rerun()

    db.close()