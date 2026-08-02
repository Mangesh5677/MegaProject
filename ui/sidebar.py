import streamlit as st


def render_sidebar():
    st.sidebar.title("🧠 AI Productivity Manager")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Tasks",
            "Fixed Timetable",
            "Calendar",
            "AI Scheduler",
            "Chatbot",
            "Analytics",
            "Settings",
        ],
    )

    return page