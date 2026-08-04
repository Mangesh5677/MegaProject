import os
import shutil
import streamlit as st

from modules.database.database import SessionLocal
from modules.database.models import User, Task


def render_settings():

    st.title("⚙ Settings")
    st.caption("Manage your account and application preferences.")

    db = SessionLocal()

    user = st.session_state.user

    # ==========================================
    # Account
    # ==========================================

    with st.expander("👤 Account Settings", expanded=True):

        st.text_input(
            "Name",
            value=user.name,
            disabled=True
        )

        st.text_input(
            "Email",
            value=user.email,
            disabled=True
        )

    # ==========================================
    # Notifications
    # ==========================================

    with st.expander("🔔 Notification Settings"):

        email_notification = st.checkbox(
            "Enable Email Notifications",
            value=True
        )

        desktop_notification = st.checkbox(
            "Enable Desktop Notifications",
            value=True
        )

        reminder24 = st.checkbox(
            "24 Hour Reminder",
            value=True
        )

        reminder2 = st.checkbox(
            "2 Hour Reminder",
            value=True
        )

        reminder30 = st.checkbox(
            "30 Minute Reminder",
            value=True
        )

        if st.button("💾 Save Notification Settings"):

            st.success("Notification settings saved.")

    # ==========================================
    # AI Settings
    # ==========================================

    with st.expander("🤖 AI Settings"):

        model = st.selectbox(
            "AI Model",
            [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant"
            ]
        )

        temperature = st.slider(
            "Creativity",
            0.0,
            1.0,
            0.4
        )

        tokens = st.slider(
            "Max Tokens",
            100,
            2000,
            600
        )

        if st.button("💾 Save AI Settings"):

            st.success("AI settings saved.")

    # ==========================================
    # Scheduler
    # ==========================================

    with st.expander("📅 Scheduler"):

        work_start = st.time_input(
            "Work Start"
        )

        work_end = st.time_input(
            "Work End"
        )

        daily_hours = st.slider(
            "Study Hours / Day",
            1,
            12,
            6
        )

        if st.button("Save Scheduler"):

            st.success("Scheduler settings saved.")

    # ==========================================
    # Database Backup
    # ==========================================

    with st.expander("💾 Database"):

        if st.button("📦 Backup Database"):

            source = "data/db/productivity.db"

            destination = "data/db/productivity_backup.db"

            shutil.copy(source, destination)

            st.success(
                "Database backup created successfully."
            )

        if os.path.exists(
            "data/db/productivity_backup.db"
        ):

            with open(
                "data/db/productivity_backup.db",
                "rb"
            ) as file:

                st.download_button(
                    "⬇ Download Backup",
                    file,
                    "productivity_backup.db"
                )

    # ==========================================
    # Delete Tasks
    # ==========================================

    with st.expander("🗑 Danger Zone"):

        st.warning(
            "This action cannot be undone."
        )

        if st.button(
            "Delete All Tasks"
        ):

            db.query(Task).delete()

            db.commit()

            st.success(
                "All tasks deleted."
            )

    # ==========================================
    # About
    # ==========================================

    with st.expander("ℹ About"):

        st.markdown(
            """
### AI Productivity Manager

Version **1.0**

Developer:
**Mangesh Shinde**

Built With:

- Streamlit
- SQLite
- SQLAlchemy
- Groq AI
- APScheduler
- Plotly
- Python
"""
        )

    db.close()