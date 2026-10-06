import streamlit as st

from modules.database.database import SessionLocal
from modules.auth.auth_service import login_user
from modules.auth.session import login
from modules.analytics.activity_service import log_activity


def render_login(required_role="user"):

    title = "Admin Login" if required_role == "admin" else "User Login"
    st.title(f"🔐 {title}")

    st.write("Welcome back!")

    email = st.text_input("📧 Email", key=f"{required_role}_login_email")

    password = st.text_input(
        "🔒 Password",
        type="password",
        key=f"{required_role}_login_password",
    )

    if st.button(
        "Login",
        use_container_width=True,
        key=f"{required_role}_login_submit",
    ):

        db = SessionLocal()

        user = login_user(
            db,
            email,
            password
        )

        if user:

            if getattr(user, "role", "user") != required_role:
                db.close()

                if required_role == "admin":
                    st.error("This account is not an administrator. Use User Login instead.")
                else:
                    st.error("This is an administrator account. Use Admin Login instead.")

                return

            # Record login activity
            log_activity(
                db,
                user.id,
                "LOGIN",
                "User logged in"
            )

            # Login user into session
            login(user)

            st.success(
                f"Welcome {user.name}"
            )

            db.close()

            st.rerun()

        else:

            db.close()

            st.error(
                "Invalid Email or Password"
            )