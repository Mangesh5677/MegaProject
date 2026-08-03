import streamlit as st


def login(user):

    st.session_state.logged_in = True
    st.session_state.user = user


def logout():

    st.session_state.logged_in = False
    st.session_state.user = None


def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )