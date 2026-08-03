import streamlit as st

from modules.database.database import SessionLocal
from modules.auth.auth_service import login_user
from modules.auth.session import login


def render_login():

    st.title("🔐 Login")

    st.write("Welcome back!")

    email = st.text_input("📧 Email")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        db = SessionLocal()

        user = login_user(
            db,
            email,
            password
        )

        db.close()

        if user:

            login(user)

            st.success(
                f"Welcome {user.name}"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Email or Password"
            )