import streamlit as st
import streamlit.components.v1 as components

from modules.database.database import SessionLocal
from modules.database.crud import (
    get_tasks,
    get_fixed_schedules,
)
from modules.ai.chatbot import get_chatbot_response


# ============================================================
# CHATBOT CSS
# ============================================================

def chatbot_css():

    st.markdown(
        """
        <style>

        .chatbot-title {
            font-size: 30px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .chatbot-subtitle {
            font-size: 15px;
            opacity: 0.7;
            margin-bottom: 15px;
        }

        .ai-online {
            color: #22c55e;
            font-weight: 600;
            font-size: 14px;
        }

        .info-box {
            padding: 16px;
            border-radius: 14px;
            background: rgba(99, 102, 241, 0.08);
            border: 1px solid rgba(99, 102, 241, 0.15);
            margin-bottom: 15px;
        }

        .footer-text {
            text-align: center;
            opacity: 0.45;
            font-size: 11px;
            margin-top: 20px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# VOICE ASSISTANT
# ============================================================

def voice_assistant():

    components.html(
        """
        <style>

        body {
            margin: 0;
            background: transparent;
            font-family: Arial, sans-serif;
        }

        .voice-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 8px;
        }

        .mic-button {
            width: 65px;
            height: 65px;
            border: none;
            border-radius: 50%;

            background:
                linear-gradient(
                    135deg,
                    #6366f1,
                    #8b5cf6
                );

            color: white;
            font-size: 27px;
            cursor: pointer;

            box-shadow:
                0 8px 25px
                rgba(99, 102, 241, 0.40);

            transition:
                transform 0.2s ease;
        }

        .mic-button:hover {
            transform: scale(1.08);
        }

        .mic-button.listening {
            background:
                linear-gradient(
                    135deg,
                    #ef4444,
                    #f97316
                );

            animation: pulse 1s infinite;
        }

        @keyframes pulse {

            0% {
                box-shadow:
                    0 0 0 0
                    rgba(239, 68, 68, 0.55);
            }

            70% {
                box-shadow:
                    0 0 0 18px
                    rgba(239, 68, 68, 0);
            }

            100% {
                box-shadow:
                    0 0 0 0
                    rgba(239, 68, 68, 0);
            }
        }

        #status {
            margin-top: 10px;
            font-size: 12px;
            color: #888;
            text-align: center;
            line-height: 1.4;
        }

        </style>


        <div class="voice-container">

            <button
                id="mic"
                class="mic-button"
                onclick="startListening()"
            >
                🎤
            </button>

            <div id="status">
                Tap microphone to speak
            </div>

        </div>


        <script>

        const mic =
            document.getElementById("mic");

        const status =
            document.getElementById("status");


        function startListening() {

            const SpeechRecognition =
                window.SpeechRecognition ||
                window.webkitSpeechRecognition;


            if (!SpeechRecognition) {

                status.innerText =
                    "❌ Voice recognition is not supported";

                return;
            }


            const recognition =
                new SpeechRecognition();


            recognition.lang =
                "en-IN";


            recognition.interimResults =
                false;


            recognition.continuous =
                false;


            mic.classList.add(
                "listening"
            );


            status.innerText =
                "🎙️ Listening...";


            recognition.start();


            recognition.onresult =
                function(event) {

                    const text =
                        event.results[0][0]
                        .transcript;


                    status.innerText =
                        "✅ " + text;


                    navigator.clipboard
                        .writeText(text);

                };


            recognition.onerror =
                function() {

                    status.innerText =
                        "❌ Could not understand voice";

                    mic.classList.remove(
                        "listening"
                    );

                };


            recognition.onend =
                function() {

                    mic.classList.remove(
                        "listening"
                    );

                };

        }

        </script>
        """,
        height=125,
    )


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak_response(text):

    # Clean response for speech
    safe_text = str(text)

    safe_text = (
        safe_text
        .replace("\\", "")
        .replace('"', "")
        .replace("'", "")
        .replace("\n", " ")
        .replace("`", "")
    )

    # Limit very long responses
    safe_text = safe_text[:1500]

    # Escape JavaScript-sensitive characters
    safe_text = (
        safe_text
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
    )

    components.html(
        f"""
        <script>

        const responseText =
            "{safe_text}";

        if (
            "speechSynthesis"
            in window
        ) {{

            window.speechSynthesis.cancel();

            const speech =
                new SpeechSynthesisUtterance(
                    responseText
                );

            speech.lang =
                "en-IN";

            speech.rate =
                1;

            speech.pitch =
                1;

            speech.volume =
                1;

            window.speechSynthesis.speak(
                speech
            );

        }}

        </script>
        """,
        height=0,
    )


# ============================================================
# MAIN CHATBOT
# ============================================================

def render_chatbot():

    # Load CSS
    chatbot_css()


    # ========================================================
    # SESSION USER
    # ========================================================

    user = st.session_state.user


    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        "## 🤖 AI Productivity Assistant"
    )

    st.caption(
        "Your intelligent assistant for tasks, timetable, "
        "planning and productivity."
    )

    st.success(
        "🟢 AI Assistant Online"
    )


    # ========================================================
    # DATABASE
    # ========================================================

    db = SessionLocal()


    try:

        # ====================================================
        # GET USER TASKS
        # ====================================================

        tasks = get_tasks(
            db,
            user.id,
        )


        # ====================================================
        # GET USER TIMETABLE
        # ====================================================

        timetable = get_fixed_schedules(
            db,
            user.id,
        )


        # ====================================================
        # TASK CONTEXT
        # ====================================================

        if tasks:

            task_text = "\n".join(
                [
                    (
                        f"- {task.title} | "
                        f"Priority: {task.priority} | "
                        f"Status: {task.status} | "
                        f"Due: {task.due_date} "
                        f"{task.due_time or ''} | "
                        f"Duration: "
                        f"{task.duration or 0} minutes"
                    )
                    for task in tasks
                ]
            )

        else:

            task_text = (
                "No tasks available."
            )


        # ====================================================
        # TIMETABLE CONTEXT
        # ====================================================

        if timetable:

            timetable_text = "\n".join(
                [
                    (
                        f"- {item.day} | "
                        f"{item.start_time} - "
                        f"{item.end_time} | "
                        f"{item.title} | "
                        f"{item.category or 'Other'}"
                    )
                    for item in timetable
                ]
            )

        else:

            timetable_text = (
                "No fixed timetable available."
            )


        # ====================================================
        # CHAT HISTORY
        # ====================================================

        if "chat_history" not in st.session_state:

            st.session_state.chat_history = []


        # ====================================================
        # SIDEBAR
        # ====================================================

        with st.sidebar:

            st.markdown(
                "### 🤖 AI Assistant"
            )


            # ------------------------------------------------
            # CLEAR CHAT
            # ------------------------------------------------

            if st.button(
                "🧹 Clear Conversation",
                use_container_width=True,
            ):

                st.session_state.chat_history = []

                st.rerun()


            st.divider()


            # ------------------------------------------------
            # VOICE ASSISTANT
            # ------------------------------------------------

            st.markdown(
                "### 🎤 Voice Assistant"
            )

            st.info(
                "🎤 Talk to your AI Assistant\n\n"
                "Click the microphone and speak."
            )

            voice_assistant()

            st.caption(
                "Voice input works best in "
                "Google Chrome or Microsoft Edge."
            )


            st.divider()


            # ------------------------------------------------
            # USER CONTEXT
            # ------------------------------------------------

            st.markdown(
                "### 📊 Your AI Context"
            )

            st.write(
                f"📋 Tasks: **{len(tasks)}**"
            )

            st.write(
                f"📅 Timetable entries: **{len(timetable)}**"
            )


        # ====================================================
        # WELCOME SCREEN
        # ====================================================

        if not st.session_state.chat_history:

            st.info(
                "👋 Welcome!\n\n"
                "I'm your personal AI productivity assistant. "
                "Ask me anything about your tasks, timetable "
                "or daily planning."
            )


            st.markdown(
                "### ✨ Try asking"
            )


            # =================================================
            # QUICK QUESTIONS
            # =================================================

            col1, col2, col3 = st.columns(3)


            with col1:

                if st.button(
                    "📋 What tasks should I do today?",
                    use_container_width=True,
                ):

                    st.session_state.quick_question = (
                        "What tasks should I do today?"
                    )

                    st.rerun()


            with col2:

                if st.button(
                    "📅 When am I free today?",
                    use_container_width=True,
                ):

                    st.session_state.quick_question = (
                        "When am I free today?"
                    )

                    st.rerun()


            with col3:

                if st.button(
                    "⭐ Which task is most important?",
                    use_container_width=True,
                ):

                    st.session_state.quick_question = (
                        "Which task is most important?"
                    )

                    st.rerun()


        # ====================================================
        # DISPLAY CHAT HISTORY
        # ====================================================

        for message in st.session_state.chat_history:

            if message["role"] == "user":

                avatar = "🧑"

            else:

                avatar = "🤖"


            with st.chat_message(
                message["role"],
                avatar=avatar,
            ):

                st.markdown(
                    message["content"]
                )


        # ====================================================
        # QUICK QUESTION
        # ====================================================

        prompt = st.session_state.pop(
            "quick_question",
            None,
        )


        # ====================================================
        # CHAT INPUT
        # ====================================================

        chat_prompt = st.chat_input(
            "💬 Ask your AI productivity assistant..."
        )


        if chat_prompt:

            prompt = chat_prompt


        # ====================================================
        # PROCESS USER MESSAGE
        # ====================================================

        if prompt:

            # -----------------------------------------------
            # SAVE USER MESSAGE
            # -----------------------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )


            # -----------------------------------------------
            # DISPLAY USER MESSAGE
            # -----------------------------------------------

            with st.chat_message(
                "user",
                avatar="🧑",
            ):

                st.write(
                    prompt
                )


            # -----------------------------------------------
            # AI RESPONSE
            # -----------------------------------------------

            with st.chat_message(
                "assistant",
                avatar="🤖",
            ):

                with st.spinner(
                    "🤖 Thinking..."
                ):

                    try:

                        response = get_chatbot_response(
                            prompt,
                            task_text,
                            timetable_text,
                        )

                    except Exception as e:

                        response = (
                            "❌ I couldn't generate "
                            "a response right now.\n\n"
                            f"Error: {str(e)}"
                        )


                # -------------------------------------------
                # DISPLAY RESPONSE
                # -------------------------------------------

                st.write(
                    response
                )


                # -------------------------------------------
                # VOICE RESPONSE
                # -------------------------------------------

                try:

                    speak_response(
                        response
                    )

                except Exception:

                    pass


            # -----------------------------------------------
            # SAVE AI RESPONSE
            # -----------------------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )


        # ====================================================
        # FOOTER
        # ====================================================

        st.caption(
            "🤖 AI Productivity Manager • "
            "Smart Planning • Voice Assistant"
        )


    finally:

        db.close()