import streamlit as st
import time


def build_aptitude_questions():
    return [
        {"question": "If 20% of a number is 40, what is the number?", "options": ["100", "200", "300", "400"], "answer": "200"},
        {"question": "A train covers 120 km in 2 hours. What is its speed?", "options": ["50 km/h", "60 km/h", "70 km/h", "80 km/h"], "answer": "60 km/h"},
        {"question": "The average of 4, 6, 8, 10 is:", "options": ["6", "7", "8", "9"], "answer": "7"},
        {"question": "What is 15% of 300?", "options": ["30", "35", "45", "60"], "answer": "45"},
        {"question": "If a book costs Rs. 250 and is discounted by 20%, what is the sale price?", "options": ["200", "210", "220", "230"], "answer": "200"},
        {"question": "A sum of money doubles in 5 years at simple interest. What is the rate of interest?", "options": ["10%", "15%", "20%", "25%"], "answer": "20%"},
        {"question": "What is the next number in the series: 2, 6, 12, 20, 30, ?", "options": ["36", "40", "42", "48"], "answer": "42"},
        {"question": "The ratio of 3:5 is equivalent to which fraction?", "options": ["0.5", "0.6", "0.8", "0.75"], "answer": "0.6"},
        {"question": "A cyclist travels 18 km in 3 hours. What is the speed in km/h?", "options": ["4", "5", "6", "7"], "answer": "6"},
        {"question": "Find the LCM of 12 and 18.", "options": ["24", "36", "48", "72"], "answer": "36"},
        {"question": "If x + 5 = 12, then x = ?", "options": ["5", "6", "7", "8"], "answer": "7"},
        {"question": "What is the square of 13?", "options": ["139", "169", "179", "196"], "answer": "169"},
        {"question": "A rectangle has length 10 and breadth 4. What is its area?", "options": ["20", "30", "40", "50"], "answer": "40"},
        {"question": "If 8 workers complete a task in 6 days, how many days will 12 workers take?", "options": ["3", "4", "5", "6"], "answer": "4"},
        {"question": "The probability of getting a head when tossing a coin is:", "options": ["0.25", "0.5", "0.75", "1"], "answer": "0.5"},
        {"question": "Which number is divisible by 9?", "options": ["123", "128", "136", "140"], "answer": "123"},
        {"question": "If a car covers 240 km in 4 hours, then the average speed is:", "options": ["40 km/h", "50 km/h", "60 km/h", "70 km/h"], "answer": "60 km/h"},
        {"question": "The value of 3^4 is:", "options": ["12", "27", "64", "81"], "answer": "81"},
        {"question": "Find the median of 5, 9, 3, 7, 1.", "options": ["3", "5", "7", "9"], "answer": "5"},
        {"question": "If 2/3 of a number is 18, then the number is:", "options": ["24", "27", "30", "36"], "answer": "27"},
        {"question": "What is 25% of 80?", "options": ["10", "15", "20", "25"], "answer": "20"},
        {"question": "The HCF of 18 and 24 is:", "options": ["2", "3", "6", "12"], "answer": "6"},
        {"question": "If a person buys 5 pens for Rs. 50, the cost of 1 pen is:", "options": ["5", "8", "10", "12"], "answer": "10"},
        {"question": "A number is increased by 10% and then decreased by 10%. What is the net change?", "options": ["0%", "1% decrease", "1% increase", "10% decrease"], "answer": "1% decrease"},
        {"question": "What is the value of 0.5 × 0.5?", "options": ["0.25", "0.5", "1", "2.5"], "answer": "0.25"},
        {"question": "Simple interest on Rs. 1000 at 5% for 2 years is:", "options": ["Rs. 50", "Rs. 75", "Rs. 100", "Rs. 150"], "answer": "Rs. 100"},
    ]


def render_career():
    st.title("💼 Career Prep Hub")
    st.caption("Smart preparation space for B.Tech students, freshers, and professionals targeting internships and full-time roles.")

    st.subheader("🔎 Search Job Roles")

    job_role = st.selectbox(
        "Choose a job role you are targeting",
        [
            "Software Engineer",
            "Data Analyst",
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "Python Developer",
            "DevOps Engineer",
            "UI/UX Designer",
            "Product Analyst",
            "Cyber Security Analyst",
            "Other",
        ],
    )

    experience_level = st.radio(
        "Career stage",
        ["B.Tech Student", "Fresher", "Working Professional"],
        horizontal=True,
    )

    job_type = st.selectbox(
        "Job Type",
        ["Internship", "Full Time", "Remote", "Hybrid", "Onsite"],
    )

    skills_input = st.text_area(
        "Add skills or keywords related to this role",
        placeholder="e.g. Python, SQL, Machine Learning, DSA, React, Java, Communication",
        height=100,
    )

    if st.button("💡 Suggest Preparation Plan"):
        skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        if not skills:
            skills = ["core concepts", "projects", "communication"]

        st.success(f"You selected: {job_role} | {experience_level} | {job_type}")

        with st.container():
            st.markdown("### Recommended preparation roadmap")
            st.markdown(f"- Focus on: {', '.join(skills[:5])}")
            st.markdown("- Build 2-3 strong projects related to this role")
            st.markdown("- Practice DSA / aptitude / communication skills")
            st.markdown("- Prepare for resume, LinkedIn, and interview questions")

    st.divider()

    st.subheader("🧠 Aptitude Test (25 Questions)")

    if "aptitude_started" not in st.session_state:
        st.session_state.aptitude_started = False
        st.session_state.aptitude_index = 0
        st.session_state.aptitude_score = 0
        st.session_state.aptitude_answers = {}
        st.session_state.aptitude_time = 900

    aptitude_questions = build_aptitude_questions()

    if not st.session_state.aptitude_started:
        if st.button("🚀 Start Aptitude Exam"):
            st.session_state.aptitude_started = True
            st.session_state.aptitude_start_time = time.time()
            st.rerun()
    else:
        elapsed = int(time.time() - st.session_state.aptitude_start_time)
        remaining = max(0, st.session_state.aptitude_time - elapsed)
        minutes, seconds = divmod(remaining, 60)

        st.info(f"⏱️ Time Remaining: {minutes:02d}:{seconds:02d}")

        if remaining <= 0:
            st.warning("⏰ Time is up! Your aptitude exam has ended.")
            st.session_state.aptitude_started = False
            final_score = 0
            for idx, item in enumerate(aptitude_questions):
                if st.session_state.aptitude_answers.get(idx) == item["answer"]:
                    final_score += 1
            st.success(f"🏁 Final score: {final_score}/{len(aptitude_questions)}")
            st.session_state.aptitude_index = 0
            st.session_state.aptitude_score = 0
            st.session_state.aptitude_answers = {}
            st.session_state.aptitude_time = 900
            st.stop()

        q_index = st.session_state.aptitude_index
        q = aptitude_questions[q_index]

        st.write(f"**Question {q_index + 1}/{len(aptitude_questions)}**")
        st.write(q["question"])

        selected = st.radio(
            "Choose the correct answer",
            q["options"],
            index=None,
            key=f"aptitude_{q_index}",
            horizontal=True,
        )

        if selected is not None:
            st.session_state.aptitude_answers[q_index] = selected

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Next Question"):
                if st.session_state.aptitude_index < len(aptitude_questions) - 1:
                    st.session_state.aptitude_index += 1
                    st.rerun()
                else:
                    final_score = 0
                    for idx, item in enumerate(aptitude_questions):
                        if st.session_state.aptitude_answers.get(idx) == item["answer"]:
                            final_score += 1
                    st.success(f"🏁 Aptitude test complete! Final score: {final_score}/{len(aptitude_questions)}")
                    st.session_state.aptitude_started = False
                    st.session_state.aptitude_index = 0
                    st.session_state.aptitude_answers = {}
                    st.session_state.aptitude_time = 900
                    st.session_state.aptitude_score = 0
                    st.stop()

        with col2:
            if st.button("Reset Exam"):
                st.session_state.aptitude_started = False
                st.session_state.aptitude_index = 0
                st.session_state.aptitude_score = 0
                st.session_state.aptitude_answers = {}
                st.session_state.aptitude_time = 900
                st.rerun()

    st.divider()

    st.subheader("🛠️ Technical Interview Questions")

    technical_bank = {
        "Software Engineer": [
            "What is the difference between a process and a thread?",
            "Explain OOP concepts in your own words.",
            "How do you optimize a slow SQL query?",
            "What is the difference between GET and POST?",
            "Explain database indexing and why it matters.",
            "How would you design a scalable backend system?",
            "What is the difference between synchronous and asynchronous programming?",
            "How do you debug a production bug?",
        ],
        "Data Analyst": [
            "What is the difference between inner join and left join?",
            "How do you clean messy data?",
            "What is normalization in a database?",
            "What is the difference between a primary key and a foreign key?",
            "How do you handle missing values in a dataset?",
            "What is the purpose of SQL subqueries?",
            "How do you measure data quality?",
            "Explain the difference between correlation and causation.",
        ],
        "Frontend Developer": [
            "What is the virtual DOM in React?",
            "How do you improve page performance?",
            "Explain CSS Flexbox and Grid.",
            "What is event bubbling and event delegation?",
            "How do you handle API calls in React?",
            "What is the difference between state and props?",
            "How do you make a website responsive?",
            "What are accessibility best practices for a web app?",
        ],
        "Backend Developer": [
            "Explain REST APIs and HTTP methods.",
            "How do you ensure application scalability?",
            "What are JWT tokens used for?",
            "How do you secure an API?",
            "Explain caching and its benefits.",
            "What is the difference between SQL and NoSQL?",
            "How do you handle concurrency in a backend service?",
            "What is load balancing and why is it used?",
        ],
        "Full Stack Developer": [
            "How do you connect frontend to backend securely?",
            "Explain authentication vs authorization.",
            "What is the role of a database in a full stack app?",
            "How do you handle state across frontend and backend?",
            "What is CI/CD and why is it important?",
            "How do you deploy a web app securely?",
            "How do you debug issues across frontend and backend?",
            "Explain the difference between monolithic and microservices architecture.",
        ],
    }

    role_for_tech = st.selectbox(
        "Select technical practice area",
        [
            "Software Engineer",
            "Data Analyst",
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
        ],
    )

    tech_questions = technical_bank.get(role_for_tech, technical_bank["Software Engineer"])

    for i, q in enumerate(tech_questions, 1):
        st.markdown(f"{i}. {q}")

    st.divider()

    st.subheader("🎤 Mock Interview Practice")

    st.write("Use this prompt to simulate a real interview:")
    st.code(
        "Act as a senior interviewer for a Frontend Developer role. Ask me 8 technical questions one by one. Questions should cover HTML, CSS, JavaScript, React, DOM, performance, responsive design, accessibility, API integration, and debugging. After each answer, give brief feedback and suggest improvement. At the end, provide a final score and a summary of strengths and weak points."
    )

    mock_question = st.text_area(
        "Interview prompt",
        value="Tell me about yourself and your projects. Explain one project in detail and why you chose it.",
        height=120,
    )

    if st.button("Generate Interview Tips"):
        tips = [
            "Keep your answer structured: introduction, project details, impact, and learning.",
            "Use the STAR method for behavioral questions.",
            "Speak confidently and explain your technical choices clearly.",
            "Mention metrics such as performance, user growth, or problem solved.",
            "Show clarity on what you learned from the project.",
            "Be ready to explain trade-offs and why you chose a particular technology.",
        ]

        st.info("### Interview guidance")
        for tip in tips:
            st.write(f"- {tip}")

    st.divider()

    st.subheader("📌 Daily Career Reminder")
    st.markdown(
        """
        Suggested daily routine:
        - 20 mins aptitude practice
        - 20 mins technical question review
        - 30 mins project or coding practice
        - 10 mins resume / interview reflection
        """
    )

    st.success("This section helps students and job seekers stay prepared while applying for internships and full-time roles.")
