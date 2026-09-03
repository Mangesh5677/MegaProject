import streamlit as st
from datetime import date, time

from modules.database.database import SessionLocal
from modules.database.crud import get_tasks


def render_calendar():

    # =====================================================
    # PAGE TITLE
    # =====================================================

    st.title("Calendar")

    st.caption(
        "View your tasks according to their scheduled date."
    )


    # =====================================================
    # LOGGED-IN USER
    # =====================================================

    user = st.session_state.user


    # =====================================================
    # DATABASE
    # =====================================================

    db = SessionLocal()

    try:

        # =================================================
        # GET ONLY LOGGED-IN USER'S TASKS
        # =================================================

        tasks = get_tasks(
            db,
            user.id
        )


        # =================================================
        # DATE SELECTOR
        # =================================================

        selected_date = st.date_input(
            "📅 Select Date",
            value=date.today()
        )


        st.divider()


        # =================================================
        # SELECTED DATE TITLE
        # =================================================

        st.subheader(
            f"📋 Tasks for {selected_date.strftime('%d %B %Y')}"
        )


        # =================================================
        # FILTER TASKS
        # =================================================

        selected_tasks = [
            task
            for task in tasks
            if task.due_date == selected_date
        ]


        # =================================================
        # NO TASKS
        # =================================================

        if not selected_tasks:

            st.info(
                "📭 No tasks scheduled for this date."
            )

            return


        # =================================================
        # TASK COUNT
        # =================================================

        st.caption(
            f"📊 Total tasks: {len(selected_tasks)}"
        )


        # =================================================
        # SORT TASKS BY TIME
        # =================================================

        sorted_tasks = sorted(
            selected_tasks,
            key=lambda x: x.due_time or time(23, 59)
        )


        # =================================================
        # DISPLAY TASKS
        # =================================================

        for task in sorted_tasks:

            # ---------------------------------------------
            # PRIORITY
            # ---------------------------------------------

            if task.priority == "High":

                priority = "🔴 HIGH"

            elif task.priority == "Medium":

                priority = "🟡 MEDIUM"

            else:

                priority = "🟢 LOW"


            # ---------------------------------------------
            # STATUS
            # ---------------------------------------------

            if task.status == "Completed":

                status = "✅ Completed"

            else:

                status = "⏳ Pending"


            # ---------------------------------------------
            # DUE TIME
            # ---------------------------------------------

            if task.due_time:

                due_time = task.due_time.strftime(
                    "%I:%M %p"
                )

            else:

                due_time = "No time specified"


            # ---------------------------------------------
            # DURATION
            # ---------------------------------------------

            if task.duration:

                duration = (
                    f"{task.duration} minutes"
                )

            else:

                duration = "Not specified"


            # =================================================
            # TASK DISPLAY
            # =================================================

            with st.container(border=True):

                st.markdown(
                    f"### 📌 {task.title}"
                )


                # Description

                if task.description:

                    st.write(
                        task.description
                    )

                else:

                    st.caption(
                        "No description"
                    )


                st.divider()


                # Task information

                col1, col2 = st.columns(2)


                with col1:

                    st.write(
                        f"⭐ Priority: **{priority}**"
                    )

                    st.write(
                        f"🕒 Due Time: **{due_time}**"
                    )


                with col2:

                    st.write(
                        f"⏱ Duration: **{duration}**"
                    )

                    st.write(
                        f"📌 Status: **{status}**"
                    )


    finally:

        db.close()