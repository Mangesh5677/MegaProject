import os
import shutil
import streamlit as st

from modules.database.database import SessionLocal
from modules.database.models import User, Task
from modules.settings.settings_service import (
    get_settings,
    save_settings,
)

def render_settings():

    st.title("⚙ Settings")
    st.caption("Manage your account and application preferences.")

    db = SessionLocal()

    user = st.session_state.user
    settings = get_settings(
    db,
    user.id
)

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
            value=settings.email_notification
        )

        desktop_notification = st.checkbox(
            "Enable Desktop Notifications",
            value=settings.desktop_notification
        )

        reminder24 = st.checkbox(
            "24 Hour Reminder",
            value=settings.reminder_24h
        )

        reminder2 = st.checkbox(
            "2 Hour Reminder",
            value=settings.reminder_2h
        )

        reminder30 = st.checkbox(
            "30 Minute Reminder",
            value=settings.reminder_30m
        )

    if st.button("💾 Save Notification Settings"):

        settings.email_notification = email_notification
        settings.desktop_notification = desktop_notification
        settings.reminder_24h = reminder24
        settings.reminder_2h = reminder2
        settings.reminder_30m = reminder30

        save_settings(db, settings)

        st.success("✅ Notification settings saved successfully.")
# ==========================================
# AI Settings
# ==========================================
    with st.expander("🤖 AI Settings"):

        models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]

        index = 0

        if settings.ai_model in models:
            index = models.index(settings.ai_model)

        model = st.selectbox(
            "AI Model",
            models,
            index=index
        )

        temperature = st.slider(
            "Creativity",
            0.0,
            1.0,
            float(settings.temperature)
        )

        tokens = st.slider(
            "Max Tokens",
            100,
            2000,
            settings.max_tokens
        )

    if st.button("💾 Save AI Settings"):

        settings.ai_model = model
        settings.temperature = str(temperature)
        settings.max_tokens = tokens

        save_settings(db, settings)

        st.success("✅ AI settings saved.")
# ==========================================
# Scheduler
# ==========================================

    with st.expander("📅 Scheduler"):

        work_start = st.time_input(
            "Work Start",
            value=settings.work_start
        )

        work_end = st.time_input(
            "Work End",
            value=settings.work_end
        )

        daily_hours = st.slider(
            "Study Hours / Day",
            1,
            12,
            settings.daily_hours
        )

    if st.button("💾 Save Scheduler"):

        settings.work_start = work_start
        settings.work_end = work_end
        settings.daily_hours = daily_hours

        save_settings(db, settings)

        st.success("✅ Scheduler settings saved.")
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