import streamlit as st
from ui.pages.ai_scheduler import render_ai_scheduler
# Database
from modules.database.database import Base, engine
import modules.database.models
from ui.pages.tasks import render_tasks
from ui.pages.ai_scheduler import render_ai_scheduler
from ui.pages.calendar import render_calendar
def load_css():
    with open("ui/styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Create all database tables
Base.metadata.create_all(bind=engine)

# UI
from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard
from ui.pages.fixed_schedule import render_fixed_schedule

st.set_page_config(
    page_title="AI Productivity Manager",
    page_icon="🧠",
    layout="wide",
)

page = render_sidebar()

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
    st.title("💬 AI Chatbot")

elif page == "Analytics":
    st.title("📊 Analytics")

elif page == "Settings":
    st.title("⚙ Settings")