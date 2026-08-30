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

    st.caption(
        "Your personal weekly timetable. "
        "Each user has a separate timetable."
    )

    user = st.session_state.user

    db = SessionLocal()

    try:

        # ========================================================
        # ADD TIMETABLE ENTRY
        # ========================================================

        with st.expander(
            "➕ Add Timetable Entry",
            expanded=True
        ):

            with st.form("fixed_schedule_form"):

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

                title = st.text_input(
                    "Subject / Event",
                    placeholder="Example: Java Lecture",
                )

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

                col1, col2 = st.columns(2)

                with col1:

                    start = st.time_input(
                        "Start Time",
                        value=time(9, 0),
                    )

                with col2:

                    end = st.time_input(
                        "End Time",
                        value=time(10, 0),
                    )

                submitted = st.form_submit_button(
                    "💾 Save Timetable",
                    use_container_width=True,
                )

                if submitted:

                    if not title.strip():

                        st.error(
                            "❌ Please enter a subject/event name."
                        )

                    elif start >= end:

                        st.error(
                            "❌ End time must be after start time."
                        )

                    else:

                        add_fixed_schedule(
                            db=db,
                            user_id=user.id,
                            day=day,
                            title=title.strip(),
                            category=category,
                            start_time=start,
                            end_time=end,
                        )

                        st.success(
                            "✅ Timetable entry saved!"
                        )

                        st.rerun()

        st.divider()

        # ========================================================
        # GET ONLY CURRENT USER'S TIMETABLE
        # ========================================================

        schedules = get_fixed_schedules(
            db,
            user.id,
        )

        st.subheader(
            f"📚 Your Timetable ({len(schedules)} entries)"
        )

        # ========================================================
        # EMPTY TIMETABLE
        # ========================================================

        if not schedules:

            st.info(
                "📅 No timetable entries yet. "
                "Add your college or personal schedule above."
            )

        else:

            # ====================================================
            # Day order
            # ====================================================

            day_order = {
                "Monday": 1,
                "Tuesday": 2,
                "Wednesday": 3,
                "Thursday": 4,
                "Friday": 5,
                "Saturday": 6,
                "Sunday": 7,
            }

            schedules.sort(
                key=lambda x: (
                    day_order.get(x.day, 99),
                    x.start_time,
                )
            )

            # ====================================================
            # Display timetable
            # ====================================================

            current_day = None

            for item in schedules:

                # -----------------------------------------------
                # Day heading
                # -----------------------------------------------

                if item.day != current_day:

                    current_day = item.day

                    st.markdown(
                        f"### 📅 {current_day}"
                    )

                col1, col2 = st.columns(
                    [6, 1]
                )

                with col1:

                    start_text = (
                        item.start_time.strftime("%H:%M")
                        if item.start_time
                        else "--:--"
                    )

                    end_text = (
                        item.end_time.strftime("%H:%M")
                        if item.end_time
                        else "--:--"
                    )

                    st.markdown(
                        f"""
                        **🕒 {start_text} → {end_text}**

                        📘 **{item.title}**

                        📂 {item.category or "Other"}
                        """
                    )

                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_schedule_{item.id}",
                        use_container_width=True,
                    ):

                        deleted = delete_fixed_schedule(
                            db,
                            user.id,
                            item.id,
                        )

                        if deleted:

                            st.success(
                                "Timetable entry deleted."
                            )

                        else:

                            st.error(
                                "Timetable entry not found."
                            )

                        st.rerun()

                st.divider()

    finally:

        db.close()