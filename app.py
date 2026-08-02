import os
import streamlit as st

# ==========================
# Database
# ==========================
from modules.database.database import Base, engine
import modules.database.models

# ==========================
# UI Imports
# ==========================
from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard

from ui.pages.tasks import render_tasks
from ui.pages.fixed_schedule import render_fixed_schedule
from ui.pages.calendar import render_calendar
from ui.pages.ai_scheduler import render_ai_scheduler
from ui.pages.analytics import render_analytics
from ui.pages.ai_advisor import render_ai_advisor
from ui.pages.chatbot import render_chatbot

# ==========================
# Streamlit Config
# ==========================
st.set_page_config(
    page_title="AI Productivity Manager",
    page_icon="🧠",
    layout="wide",
)

# ==========================
# Load CSS
# ==========================
def load_css():
    css_path = os.path.join("ui", "styles", "style.css")

    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css()

# ==========================
# Create Database Tables
# ==========================
Base.metadata.create_all(bind=engine)

# ==========================
# Sidebar Navigation
# ==========================
page = render_sidebar()

# ==========================
# Routing
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
    st.title("⚙️ Settings")