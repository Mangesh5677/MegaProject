import streamlit as st

from modules.database.database import SessionLocal
from modules.auth.auth_service import register_user


def render_register():

    st.title("📝 Create Account")

    name = st.text_input(
        "Full Name"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button(
        "Register",
        use_container_width=True
    ):

        if password != confirm:

            st.error(
                "Passwords do not match."
            )

            return

        db = SessionLocal()

        success, message = register_user(
            db,
            name,
            email,
            password
        )

        db.close()

        if success:

            st.success(message)

        else:

            st.error(message)