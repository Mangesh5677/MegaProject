import streamlit as st

try:
    from streamlit_mic_recorder import speech_to_text
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

from modules.ai.voice import speak
from modules.database.database import SessionLocal
from modules.ai.chatbot import build_context
from modules.ai.groq_service import ask_ai


def render_chatbot():

    st.title("💬 AI Productivity Assistant")

    st.markdown("""
Welcome! I can help you with:

- 📋 Task Management
- 📅 Study Planning
- 🤖 AI Scheduling
- ⏰ Deadlines
- 📈 Productivity Analysis
- 🎯 Time Management
""")

    db = SessionLocal()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ==========================
    # Quick Questions
    # ==========================

    st.subheader("⚡ Quick Questions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 Pending Tasks", use_container_width=True):
            st.session_state["quick_prompt"] = "Show my pending tasks."

    with col2:
        if st.button("📅 Plan Today", use_container_width=True):
            st.session_state["quick_prompt"] = "Create today's study plan."

    with col3:
        if st.button("📈 Productivity", use_container_width=True):
            st.session_state["quick_prompt"] = "Analyze my productivity."

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("🎯 Highest Priority", use_container_width=True):
            st.session_state["quick_prompt"] = "Which task should I do first?"

    with col5:
        if st.button("⏰ Deadlines", use_container_width=True):
            st.session_state["quick_prompt"] = "Show upcoming deadlines."

    with col6:
        if st.button("🧠 Study Tips", use_container_width=True):
            st.session_state["quick_prompt"] = "Give me study tips."

    st.divider()

    # ==========================
    # Voice Assistant
    # ==========================

    st.subheader("🎤 Voice Assistant")

    voice_text = speech_to_text(
        language="en",
        start_prompt="🎙 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True,
        use_container_width=True,
    )

    if voice_text:
        st.success(f"🎤 You said: {voice_text}")
        st.session_state["quick_prompt"] = voice_text

    st.divider()

    # ==========================
    # Chat History
    # ==========================

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask anything...")

    if not prompt:
        prompt = st.session_state.pop("quick_prompt", None)

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        context = build_context(db)

        with st.chat_message("assistant"):

            with st.spinner("🤖 AI is thinking..."):

                try:

                    answer = ask_ai(
                        context,
                        prompt
                    )

                except Exception as e:

                    answer = f"❌ Error:\n\n{e}"

                st.markdown(answer)

                # ==========================
                # Voice Output
                # ==========================

                try:

                    audio_path = speak(answer)

                    with open(audio_path, "rb") as audio_file:
                        st.audio(
                            audio_file.read(),
                            format="audio/mp3"
                        )

                except Exception as e:
                    st.warning(f"Voice Error: {e}")

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💬 Messages",
            len(st.session_state.messages)
        )

    with col2:
        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    db.close()