import streamlit as st

from modules.database.database import SessionLocal

from modules.database.crud import (
    get_tasks,
    get_fixed_schedules,
)

from modules.ai.chatbot import (
    get_chatbot_response,
)

from modules.ai.resources import (
    get_task_resources,
)


# ============================================================
# Helper: Get User ID
# ============================================================

def get_user_id(user):

    if hasattr(user, "id"):

        return user.id

    if isinstance(user, dict):

        return user.get("id")

    return None


# ============================================================
# Helper: Display YouTube Resources
# ============================================================

def display_youtube_resources(resources):

    videos = resources.get(
        "youtube_videos",
        []
    )

    youtube_search = resources.get(
        "youtube_search"
    )

    if videos:

        st.markdown(
            "#### 🎥 Recommended YouTube Videos"
        )

        # Display maximum 3 videos
        for video in videos[:3]:

            title = video.get(
                "title",
                "YouTube Video"
            )

            channel = video.get(
                "channel",
                "YouTube"
            )

            url = video.get(
                "url"
            )

            thumbnail = video.get(
                "thumbnail"
            )

            # ----------------------------------------------
            # Video Card
            # ----------------------------------------------

            video_col1, video_col2 = st.columns(
                [1, 2]
            )

            with video_col1:

                if thumbnail:

                    st.image(
                        thumbnail,
                        use_container_width=True
                    )

            with video_col2:

                st.markdown(
                    f"**{title}**"
                )

                st.caption(
                    f"📺 {channel}"
                )

                if url:

                    st.link_button(
                        "▶️ Watch on YouTube",
                        url,
                        use_container_width=True
                    )

            st.divider()

    elif youtube_search:

        st.info(
            "No direct videos were found. "
            "You can search YouTube for this task."
        )

        st.link_button(
            "🔎 Search YouTube",
            youtube_search,
            use_container_width=True
        )


# ============================================================
# Helper: Display LeetCode Resources
# ============================================================

def display_leetcode_resources(resources):

    leetcode = resources.get(
        "leetcode"
    )

    if not leetcode:

        return

    st.markdown(
        "#### 💻 LeetCode Practice"
    )

    st.info(
        "This task looks like a coding/DSA task. "
        "Here are relevant LeetCode resources."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.link_button(
            "🚀 Open LeetCode",
            leetcode["problemset"],
            use_container_width=True
        )

    with col2:

        st.link_button(
            "🔎 Search Problems",
            leetcode["search"],
            use_container_width=True
        )


# ============================================================
# Helper: Display Resources For Task
# ============================================================

def display_task_resources(task):

    resources = get_task_resources(
        task
    )

    resource_type = resources.get(
        "type",
        "general"
    )

    # ========================================================
    # Fitness
    # ========================================================

    if resource_type == "fitness":

        st.markdown(
            "### 🏋️ Fitness Resources"
        )

        st.caption(
            "Helpful workout videos related to this task."
        )

        display_youtube_resources(
            resources
        )

    # ========================================================
    # Coding
    # ========================================================

    elif resource_type == "coding":

        st.markdown(
            "### 💻 Coding Resources"
        )

        display_leetcode_resources(
            resources
        )

        display_youtube_resources(
            resources
        )

    # ========================================================
    # Study
    # ========================================================

    elif resource_type == "study":

        st.markdown(
            "### 📚 Learning Resources"
        )

        display_youtube_resources(
            resources
        )

    # ========================================================
    # General
    # ========================================================

    else:

        st.markdown(
            "### 🔎 Helpful Resources"
        )

        display_youtube_resources(
            resources
        )


# ============================================================
# Chatbot Page
# ============================================================

def render_chatbot():

    # ========================================================
    # Page Header
    # ========================================================

    st.title(
        "🤖 AI Productivity Assistant"
    )

    st.caption(
        "Your personal AI assistant for tasks, schedules, "
        "learning and productivity."
    )

    # ========================================================
    # Session State
    # ========================================================

    if "chat_messages" not in st.session_state:

        st.session_state.chat_messages = []

    # ========================================================
    # Logged-in User
    # ========================================================

    user = st.session_state.user

    user_id = get_user_id(
        user
    )

    if user_id is None:

        st.error(
            "Unable to identify the logged-in user."
        )

        return

    # ========================================================
    # Database
    # ========================================================

    db = SessionLocal()

    try:

        # ====================================================
        # Get User Data
        # ====================================================

        tasks = get_tasks(
            db,
            user_id
        )

        fixed_schedules = get_fixed_schedules(
            db,
            user_id
        )

        # ====================================================
        # Statistics
        # ====================================================

        total_tasks = len(
            tasks
        )

        pending_tasks = sum(
            1
            for task in tasks
            if task.status != "Completed"
        )

        completed_tasks = sum(
            1
            for task in tasks
            if task.status == "Completed"
        )

        # ====================================================
        # Statistics Cards
        # ====================================================

        col1, col2, col3 = st.columns(
            3
        )

        with col1:

            st.metric(
                "📋 Total Tasks",
                total_tasks
            )

        with col2:

            st.metric(
                "⏳ Pending",
                pending_tasks
            )

        with col3:

            st.metric(
                "✅ Completed",
                completed_tasks
            )

        st.divider()

        # ====================================================
        # Quick Questions
        # ====================================================

        st.subheader(
            "⚡ Quick Questions"
        )

        q1, q2, q3, q4 = st.columns(
            4
        )

        with q1:

            if st.button(
                "📅 Today's Tasks",
                use_container_width=True
            ):

                st.session_state.quick_question = (
                    "What tasks should I do today?"
                )

        with q2:

            if st.button(
                "🔥 Priorities",
                use_container_width=True
            ):

                st.session_state.quick_question = (
                    "Which tasks should I prioritize?"
                )

        with q3:

            if st.button(
                "⏰ Schedule",
                use_container_width=True
            ):

                st.session_state.quick_question = (
                    "Help me plan my remaining tasks "
                    "around my fixed timetable."
                )

        with q4:

            if st.button(
                "📊 Progress",
                use_container_width=True
            ):

                st.session_state.quick_question = (
                    "How is my productivity progress?"
                )

        st.divider()

        # ====================================================
        # Chat Header
        # ====================================================

        st.subheader(
            "💬 Chat with your AI Assistant"
        )

        # ====================================================
        # Welcome Message
        # ========================================================

        if not st.session_state.chat_messages:

            with st.chat_message(
                "assistant",
                avatar="🤖"
            ):

                st.markdown(
                    """
### 👋 Hello!

I'm your **AI Productivity Assistant**.

I can help you with:

- 📋 Understand your tasks
- 📅 Plan today's work
- 🔥 Find high-priority tasks
- ⏰ Plan around your college timetable
- 🎯 Improve productivity
- 📊 Review your progress
- 🎥 Find useful YouTube learning videos
- 💻 Find LeetCode practice resources

### Try asking me:

> **What tasks should I do today?**

or

> **Help me with my LeetCode task.**

or

> **Give me a workout video for my gym task.**
"""
                )

        # ====================================================
        # Display Chat History
        # ====================================================

        for message in st.session_state.chat_messages:

            if message["role"] == "user":

                with st.chat_message(
                    "user",
                    avatar="🧑"
                ):

                    st.markdown(
                        message["content"]
                    )

            else:

                with st.chat_message(
                    "assistant",
                    avatar="🤖"
                ):

                    st.markdown(
                        message["content"]
                    )

        # ====================================================
        # Quick Question
        # ====================================================

        quick_question = st.session_state.pop(
            "quick_question",
            None
        )

        # ====================================================
        # Chat Input
        # ====================================================

        user_prompt = st.chat_input(
            "Ask about your tasks, schedule or learning..."
        )

        if quick_question:

            user_prompt = quick_question

        # ====================================================
        # Generate AI Response
        # ====================================================

        if user_prompt:

            # ------------------------------------------------
            # Save User Message
            # ------------------------------------------------

            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": user_prompt
                }
            )

            # ------------------------------------------------
            # Display User Message
            # ------------------------------------------------

            with st.chat_message(
                "user",
                avatar="🧑"
            ):

                st.markdown(
                    user_prompt
                )

            # ------------------------------------------------
            # AI Response
            # ------------------------------------------------

            with st.chat_message(
                "assistant",
                avatar="🤖"
            ):

                with st.spinner(
                    "🤔 Thinking about your tasks..."
                ):

                    response = get_chatbot_response(
                        user_message=user_prompt,
                        tasks=tasks,
                        fixed_schedules=fixed_schedules,
                        chat_history=(
                            st.session_state
                            .chat_messages[:-1]
                        )
                    )

                st.markdown(
                    response
                )

            # ------------------------------------------------
            # Save AI Response
            # ------------------------------------------------

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            # ------------------------------------------------
            # Resource Recommendation
            # ------------------------------------------------

            st.divider()

            st.subheader(
                "🎯 Recommended Resources"
            )

            pending_tasks = [
                task
                for task in tasks
                if task.status != "Completed"
            ]

            if not pending_tasks:

                st.success(
                    "🎉 You have completed all your tasks!"
                )

            else:

                # --------------------------------------------
                # Show resources for matching tasks
                # --------------------------------------------

                for task in pending_tasks:

                    task_title = (
                        task.title
                        or "Untitled Task"
                    )

                    task_description = (
                        task.description
                        or ""
                    )

                    # Combine text
                    task_text = (
                        f"{task_title} "
                        f"{task_description}"
                    ).lower()

                    # ----------------------------------------
                    # Determine whether this task is relevant
                    # ----------------------------------------

                    user_text = (
                        user_prompt
                        .lower()
                    )

                    relevant = False

                    # Match task title
                    if task_title.lower() in user_text:

                        relevant = True

                    # Match words from task
                    task_words = [
                        word
                        for word in task_title.lower().split()
                        if len(word) > 3
                    ]

                    if any(
                        word in user_text
                        for word in task_words
                    ):

                        relevant = True

                    # General questions
                    general_questions = [
                        "today",
                        "tasks",
                        "prioritize",
                        "priority",
                        "schedule",
                        "productivity",
                        "progress",
                    ]

                    if any(
                        keyword in user_text
                        for keyword in general_questions
                    ):

                        relevant = True

                    # ----------------------------------------
                    # Show Resource Card
                    # ----------------------------------------

                    if relevant:

                        with st.container(
                            border=True
                        ):

                            st.markdown(
                                f"## 📝 {task_title}"
                            )

                            if task_description:

                                st.caption(
                                    task_description
                                )

                            # --------------------------------
                            # Task Metadata
                            # --------------------------------

                            meta1, meta2, meta3 = st.columns(
                                3
                            )

                            with meta1:

                                st.write(
                                    f"🔥 {task.priority}"
                                )

                            with meta2:

                                if task.due_date:

                                    st.write(
                                        f"📅 {task.due_date}"
                                    )

                            with meta3:

                                if task.duration:

                                    st.write(
                                        f"⏱️ {task.duration} min"
                                    )

                            # --------------------------------
                            # Generate Resources
                            # --------------------------------

                            try:

                                with st.spinner(
                                    "🔎 Finding useful resources..."
                                ):

                                    display_task_resources(
                                        task
                                    )

                            except Exception as resource_error:

                                st.warning(
                                    "Unable to load resources "
                                    "for this task."
                                )

                                st.caption(
                                    str(resource_error)
                                )

        # ====================================================
        # Resource Explorer
        # ====================================================

        st.divider()

        with st.expander(
            "🎯 Explore Resources For My Tasks"
        ):

            st.caption(
                "Get YouTube videos and coding resources "
                "for your pending tasks."
            )

            pending_tasks = [
                task
                for task in tasks
                if task.status != "Completed"
            ]

            if not pending_tasks:

                st.success(
                    "🎉 No pending tasks!"
                )

            else:

                selected_task = st.selectbox(
                    "Choose a task",
                    pending_tasks,
                    format_func=lambda task: (
                        f"{task.title} "
                        f"({task.priority})"
                    )
                )

                if st.button(
                    "🔎 Find Resources",
                    use_container_width=True
                ):

                    with st.spinner(
                        "🔎 Finding resources..."
                    ):

                        try:

                            display_task_resources(
                                selected_task
                            )

                        except Exception as e:

                            st.error(
                                f"Unable to find resources: {e}"
                            )

        # ====================================================
        # Clear Conversation
        # ====================================================

        if st.session_state.chat_messages:

            st.divider()

            if st.button(
                "🗑️ Clear Conversation",
                use_container_width=True
            ):

                st.session_state.chat_messages = []

                st.rerun()

    except Exception as e:

        st.error(
            f"Unable to load chatbot data: {e}"
        )

    finally:

        db.close()