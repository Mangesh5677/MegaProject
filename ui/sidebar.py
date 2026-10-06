from html import escape
from pathlib import Path

import streamlit as st

from modules.auth.profile import profile_photo_data_uri


def render_sidebar():
    project_logo = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "project-logo.png"
    )
    st.sidebar.image(str(project_logo), width=140)
    st.sidebar.title("AI Productivity Manager")
    user = st.session_state.get("user")

    if user and getattr(user, "role", "user") == "admin":
        pages = ["Admin Dashboard", "Settings"]
    else:
        pages = [
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
        ]

    default_page = (
        "Admin Dashboard"
        if user and getattr(user, "role", "user") == "admin"
        else "Fixed Timetable"
    )

    page = st.sidebar.radio(
        "Navigation",
        pages,
        index=pages.index(default_page),
    )

    return page


def render_user_profile(user):
    role_label = " (Admin)" if getattr(user, "role", "user") == "admin" else ""
    st.sidebar.markdown(
        f"""
        <div class="user-profile-widget">
            <img src="{profile_photo_data_uri(user.id)}" alt="Profile photo">
            <span>{escape(user.name)}{role_label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )