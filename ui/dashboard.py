import streamlit as st
from modules.database.database import SessionLocal
from modules.database.models import Task, FixedSchedule


def render_dashboard():

    db = SessionLocal()

    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "Completed").count()
    pending_tasks = db.query(Task).filter(Task.status == "Pending").count()

    productivity = 0

    if total_tasks > 0:
        productivity = int((completed_tasks / total_tasks) * 100)

    total_classes = db.query(FixedSchedule).count()

    st.title("🧠 AI Productivity Manager")
    st.caption("Your Personal AI Study Assistant")

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <h4>📋 Total Tasks</h4>
            <h1>{total_tasks}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <h4>⏳ Pending</h4>
            <h1>{pending_tasks}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <h4>✅ Completed</h4>
            <h1>{completed_tasks}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="glass-card">
            <h4>⚡ Productivity</h4>
            <h1>{productivity}%</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📅 Weekly Timetable")

        schedules = db.query(FixedSchedule).all()

        if schedules:

            for item in schedules:

                st.markdown(f"""
                <div class="glass-card">
                <b>{item.day}</b><br>
                📚 {item.title}<br>
                🕒 {item.start_time} - {item.end_time}
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("No timetable added.")

    with right:

        st.subheader("🤖 AI Suggestions")

        if pending_tasks == 0:

            st.success("🎉 Great! No pending tasks.")

        else:

            st.warning(f"""
You have **{pending_tasks} pending task(s)**.

Click **AI Scheduler**
to generate today's study plan.
""")

        st.markdown("### 💡 Quick Tips")

        st.info("✔ Complete High Priority Tasks First")

        st.info("📖 Study for 50 mins + 10 mins Break")

        st.info("💧 Drink Water Every Hour")

    db.close()