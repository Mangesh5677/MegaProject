import streamlit as st
from datetime import time

from modules.database.database import SessionLocal
from modules.database.crud import (
    add_fixed_schedule,
    get_fixed_schedules,
    delete_fixed_schedule,
)


def render_fixed_schedule():

    st.title("📅 Fixed Weekly Timetable")

    db = SessionLocal()
    user_id = st.session_state.user.id

    # ==========================================
    # Add Timetable
    # ==========================================

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
                "Sunday",
            ],
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
                "Other",
            ],
        )

        start = st.time_input(
            "Start Time",
            value=time(9, 0),
        )

        end = st.time_input(
            "End Time",
            value=time(10, 0),
        )

        submitted = st.form_submit_button("💾 Save")

        if submitted:

            add_fixed_schedule(
                db,
                user_id,
                day,
                title,
                category,
                start,
                end,
            )

            st.success("✅ Timetable Saved")
            st.rerun()

    st.divider()

    # ==========================================
    # Weekly Timetable
    # ==========================================

    st.subheader("📅 Weekly Timetable")

    schedules = get_fixed_schedules(
        db,
        user_id,
    )

    if not schedules:
        st.info("No timetable added yet.")
    else:

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        for day in days:

            st.markdown(f"### {day}")

            day_events = [
                item for item in schedules
                if item.day == day
            ]

            if not day_events:
                st.caption("No events")
                continue

            for item in day_events:

                col1, col2 = st.columns([8, 1])

                with col1:
                    st.write(
                        f"🕒 **{item.start_time.strftime('%H:%M')} - "
                        f"{item.end_time.strftime('%H:%M')}**"
                    )
                    st.write(
                        f"📘 **{item.title}** ({item.category})"
                    )

                with col2:
                    if st.button(
                        "🗑",
                        key=f"delete_{item.id}",
                    ):
                        delete_fixed_schedule(
                            db,
                            item.id,
                        )
                        st.rerun()

            st.divider()

    db.close()