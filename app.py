import streamlit as st

# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="AI Productivity Manager",
    page_icon="🧠",
    layout="wide",
)

# ==========================
# Database
# ==========================

from modules.database.database import Base, engine
import modules.database.models

Base.metadata.create_all(bind=engine)

# ==========================
# Load CSS
# ==========================

def load_css():
    with open("ui/styles/style.css") as f:
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

    st.title("🧠 AI Productivity Manager")

    tab1, tab2 = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )

    with tab1:
        render_login()

    with tab2:
        render_register()

    st.stop()

# ==========================
# Import Main Pages
# ==========================

from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard

from ui.pages.tasks import render_tasks
from ui.pages.fixed_schedule import render_fixed_schedule
from ui.pages.calendar import render_calendar
from ui.pages.analytics import render_analytics
from ui.pages.ai_scheduler import render_ai_scheduler
from ui.pages.ai_advisor import render_ai_advisor
from ui.pages.chatbot import render_chatbot

# ==========================
# Sidebar
# ==========================

page = render_sidebar()

st.sidebar.success(
    f"👋 {st.session_state.user.name}"
)

if st.sidebar.button("🚪 Logout"):

    logout()

    st.rerun()

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

elif page == "Settings":

    st.title("⚙ Settings")