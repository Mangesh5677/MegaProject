import streamlit as st

from modules.database.database import SessionLocal
from modules.dashboard.dashboard_service import get_dashboard_data


def card(title, value, icon, color):

    st.markdown(
        f"""
<div class="glass-card">

<div class="card-icon">{icon}</div>

<div class="card-title">{title}</div>

<div class="card-value">{value}</div>

</div>
""",
        unsafe_allow_html=True,
    )


def render_dashboard():

    db = SessionLocal()

    data = get_dashboard_data(db)

    st.title("🧠 AI Productivity Manager")

    st.caption("Welcome back, Mangesh 👋")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        card("Total Tasks", data["total"], "📋", "#2563eb")

    with c2:
        card("Pending", data["pending"], "⏳", "#f59e0b")

    with c3:
        card("Completed", data["completed"], "✅", "#22c55e")

    with c4:
        card("Productivity", f"{data['productivity']}%", "⚡", "#7c3aed")

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📅 Today's Timetable")

        if len(data["today_classes"]) == 0:

            st.info("No classes today")

        else:

            for cls in data["today_classes"]:

                st.markdown(
                    f"""
<div class="schedule-card">

🕒 <b>{cls.start_time.strftime('%H:%M')}</b>

➡

<b>{cls.end_time.strftime('%H:%M')}</b>

<br>

📘 {cls.title}

</div>
""",
                    unsafe_allow_html=True,
                )

    with right:

        st.subheader("🎯 Today's Goal")

        st.progress(data["productivity"] / 100)

        st.write(f"### {data['productivity']}% Completed")

        if data["pending"] == 0:

            st.success("🎉 All tasks completed")

        else:

            st.warning(f"{data['pending']} Tasks Remaining")

    st.divider()

    st.subheader("🤖 AI Recommendation")

    if data["pending"] == 0:

        st.success("Enjoy your day! Everything is completed.")

    else:

        st.info(
            f"""
Complete **High Priority** tasks first.

You currently have **{data['pending']} pending tasks**.

Use your free college slots wisely.
"""
        )

    db.close()