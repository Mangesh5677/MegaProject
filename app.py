import base64
from pathlib import Path

import streamlit as st
from modules.notifications.scheduler import start_scheduler
from ui.pages.settings import render_settings

PROJECT_ROOT = Path(__file__).resolve().parent
PROJECT_LOGO = PROJECT_ROOT / "assets" / "project-logo.png"

# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="AI Productivity Manager",
    page_icon=str(PROJECT_LOGO),
    layout="wide",
)

# ==========================
# Database
# ==========================

from modules.database.database import Base, engine
import modules.database.models

Base.metadata.create_all(bind=engine)

if "scheduler_started" not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True

# ==========================
# Load CSS
# ==========================

def load_css():
    with open("ui/styles/theme.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

load_css()

# ==========================
# Authentication
# ==========================

from modules.auth.session import (
    is_logged_in,
    logout,
)

from ui.pages.login import render_login
from ui.pages.register import render_register

# ==========================
# Login Screen
# ==========================

if not is_logged_in():
    logo_data = base64.b64encode(PROJECT_LOGO.read_bytes()).decode("ascii")

    st.markdown(
        f"""
        <div class="auth-brand">
            <img class="brand-mark" src="data:image/png;base64,{logo_data}" alt="AI Productivity Manager logo">
            <div class="brand-text">AI Productivity Manager</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "User Login",
            "Admin Login",
            "Register"
        ]
    )

    with tab1:
        render_login(required_role="user")

    with tab2:
        render_login(required_role="admin")

    with tab3:
        render_register()

    st.stop()

# ==========================
# Import Main Pages
# ==========================

from ui.sidebar import render_sidebar, render_user_profile
from ui.pages.dashboard import render_dashboard

from ui.pages.tasks import render_tasks
from ui.pages.fixed_schedule import render_fixed_schedule
from ui.pages.calendar import render_calendar
from ui.pages.analytics import render_analytics
from ui.pages.ai_scheduler import render_ai_scheduler
from ui.pages.ai_advisor import render_ai_advisor
from ui.pages.chatbot import render_chatbot
from ui.pages.career import render_career
from ui.pages.rewards import render_rewards
from ui.pages.admin_dashboard import render_admin_dashboard

user = st.session_state.user
page = render_sidebar()
render_user_profile(user)

if st.sidebar.button("🚪 Logout"):
    logout()
    st.rerun()

if getattr(user, "role", "user") == "admin":
    if page == "Settings":
        render_settings()
    else:
        render_admin_dashboard()
    st.stop()

# ==========================
# Sidebar
# ==========================

# ==========================
# Navigation
# ==========================
if page == "Dashboard":

    render_dashboard()

elif page == "Tasks":

    render_tasks()

elif page == "Fixed Timetable":

    render_fixed_schedule()

elif page == "Calendar":

    render_calendar()

elif page == "AI Scheduler":

    render_ai_scheduler()

elif page == "Chatbot":

    render_chatbot()

elif page == "Analytics":

    render_analytics()

elif page == "AI Advisor":

    render_ai_advisor()

elif page == "Career Prep":

    render_career()

elif page == "Rewards":

    render_rewards()

elif page == "Settings":

    render_settings()
