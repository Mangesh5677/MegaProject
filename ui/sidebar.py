import streamlit as st


def render_sidebar():
    st.sidebar.title("AI Productivity Manager")

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
            "Career Prep",
            "Rewards",
            "Settings",
        ],
        index=2,   # Default page = Fixed Timetable
    )

    return page
