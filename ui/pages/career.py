import random
import streamlit as st
import time
from datetime import date

from modules.database.database import SessionLocal
from modules.career.application_service import (
    apply_for_internship,
    get_applications,
    update_application,
)
from modules.career.internship_service import (
    create_internship,
    get_internships,
    update_internship_status,
)
from modules.career.preparation_service import (
    create_preparation_task,
    get_preparation_tasks,
    get_task_resources,
    set_preparation_completed,
)


ROLE_LEARNING_LINKS = {
    "Software Engineer": [
        {
            "title": "DSA for Placements - Full Roadmap",
            "url": "https://www.youtube.com/results?search_query=dsa+for+placements+roadmap",
            "description": "Learn the core coding topics required in technical interviews and coding rounds.",
        },
        {
            "title": "Aptitude & Logical Reasoning Practice",
            "url": "https://www.youtube.com/results?search_query=aptitude+questions+for+placements+youtube",
            "description": "Improve time-based problem solving for selection tests and aptitude rounds.",
        },
        {
            "title": "System Design Basics",
            "url": "https://www.youtube.com/results?search_query=system+design+for+beginners+youtube",
            "description": "Understand scalable backend design and interview-ready architecture thinking.",
        },
    ],
    "Frontend Developer": [
        {
            "title": "HTML CSS JavaScript Full Course",
            "url": "https://www.youtube.com/results?search_query=html+css+javascript+full+course+for+beginners",
            "description": "Build a strong base in front-end fundamentals and UI logic.",
        },
        {
            "title": "React JS Interview Preparation",
            "url": "https://www.youtube.com/results?search_query=react+js+interview+questions+youtube",
            "description": "Practice the most important React concepts and front-end patterns.",
        },
        {
            "title": "Responsive Design & Accessibility",
            "url": "https://www.youtube.com/results?search_query=responsive+design+accessibility+web+development",
            "description": "Improve design quality, responsiveness, and user-friendly interactions.",
        },
    ],
    "Backend Developer": [
        {
            "title": "Java / Python Backend Roadmap",
            "url": "https://www.youtube.com/results?search_query=backend+development+roadmap+for+beginners",
            "description": "Learn APIs, databases, authentication, and server-side architecture.",
        },
        {
            "title": "REST API & Database Design",
            "url": "https://www.youtube.com/results?search_query=rest+api+database+design+tutorial",
            "description": "Master endpoints, data modeling, and real-world backend patterns.",
        },
        {
            "title": "Interview Questions for Backend Roles",
            "url": "https://www.youtube.com/results?search_query=backend+developer+interview+questions+youtube",
            "description": "Prepare for practical backend and system design questions.",
        },
    ],
    "Data Analyst": [
        {
            "title": "SQL for Data Analysis",
            "url": "https://www.youtube.com/results?search_query=sql+for+data+analysis+tutorial",
            "description": "Learn joins, reporting, filtering, and analytics queries.",
        },
        {
            "title": "Excel + Power BI for Analytics",
            "url": "https://www.youtube.com/results?search_query=excel+power+bi+for+data+analytics+tutorial",
            "description": "Practice business dashboards, data cleaning, and analysis workflows.",
        },
        {
            "title": "Statistics for Interviews",
            "url": "https://www.youtube.com/results?search_query=statistics+for+data+analyst+interview",
            "description": "Reinforce probability, distributions, and interpretation questions.",
        },
    ],
    "Full Stack Developer": [
        {
            "title": "Full Stack Developer Roadmap",
            "url": "https://www.youtube.com/results?search_query=full+stack+developer+roadmap+2025",
            "description": "Understand both frontend and backend foundations with a practical roadmap.",
        },
        {
            "title": "Node.js + React Projects",
            "url": "https://www.youtube.com/results?search_query=nodejs+react+full+stack+project+tutorial",
            "description": "Build end-to-end projects and gain confidence in full-stack workflows.",
        },
        {
            "title": "Deployment & DevOps Basics",
            "url": "https://www.youtube.com/results?search_query=deployment+devops+for+fullstack+developers",
            "description": "Learn CI/CD, hosting, environment setup, and deployment fundamentals.",
        },
    ],
}

TECHNICAL_ANSWER_GUIDES = {
    "Software Engineer": {
        "What is the difference between a process and a thread?": "A process is an independent program with its own memory space, while a thread is a lightweight unit of execution within a process that shares the same memory. Threads are faster to create and communicate with, but they require careful synchronization to avoid race conditions.",
        "Explain OOP concepts in your own words.": "OOP organizes code into objects that combine data and behavior. The main concepts are encapsulation, inheritance, polymorphism, and abstraction. This makes the system easier to maintain, reuse, and scale.",
        "How do you optimize a slow SQL query?": "I would first check the query plan, identify missing indexes, reduce unnecessary joins or data, avoid SELECT *, and filter early. Then I would use indexing, proper joins, and query rewriting to reduce execution time.",
        "What is the difference between GET and POST?": "GET retrieves data and is usually used for safe, idempotent requests, while POST sends data to create or update a resource. GET includes parameters in the URL, whereas POST sends them in the request body.",
        "How do you debug a production bug?": "I would first reproduce the issue, gather logs and metrics, narrow the scope, and check recent deployments or config changes. Then I would isolate the root cause, fix the issue, validate the fix, and monitor the system afterward.",
        "Explain database indexing and why it matters.": "An index is a data structure that speeds up lookups by reducing the amount of data scanned. It helps when filtering, sorting, or joining large tables, but too many indexes can slow writes and increase storage usage.",
        "How do you design a scalable backend system?": "I would design the system with clear modules, stateless services, a database layer, caching, load balancing, and horizontal scaling. I would also consider asynchronous processing, monitoring, and reliability for future growth.",
        "What is the difference between synchronous and asynchronous programming?": "Synchronous code executes in sequence and blocks until each task finishes, while asynchronous code allows other work to continue while waiting. Asynchronous programming helps improve responsiveness and performance in I/O-heavy systems.",
    },
    "Frontend Developer": {
        "What is the virtual DOM in React?": "The virtual DOM is a lightweight copy of the real DOM used by React to optimize updates. React compares the previous and next virtual DOM states and updates only the changed parts, making UI rendering faster and more efficient.",
        "How do you improve page performance?": "I would reduce unnecessary re-renders, compress images, lazy load content, use code splitting, and avoid heavy animations. I would also profile the app with browser tools and optimize APIs and assets where needed.",
        "Explain CSS Flexbox and Grid.": "Flexbox is ideal for arranging elements in one dimension, such as row or column layouts. CSS Grid is better for complex two-dimensional layouts, where rows and columns need coordinated positioning.",
        "What is event bubbling and event delegation?": "Event bubbling means an event moves up the DOM tree from the target element to parent elements. Event delegation uses a parent element to handle events from child elements efficiently, which improves performance and reduces listeners.",
        "How do you handle API calls in React?": "I use hooks like useEffect or libraries such as Axios or fetch to call APIs, manage loading and error states, and update the UI after data arrives. I usually keep the data flow predictable and handle edge cases cleanly.",
        "What is the difference between state and props?": "State is local and mutable data inside a component, while props are read-only inputs passed from a parent component. State drives dynamic behavior within a component, while props allow reusability.",
        "How do you make a website responsive?": "I use flexible layouts, CSS media queries, relative units like percentages, and responsive design patterns such as grid and flexbox. The goal is to adapt the layout to different screen sizes without losing usability.",
        "What are accessibility best practices for a web app?": "I ensure keyboard navigation, proper color contrast, semantic HTML, labels for form controls, alt text for images, and focus states. Accessibility improves usability for everyone, including users with disabilities.",
    },
    "Backend Developer": {
        "Explain REST APIs and HTTP methods.": "REST is an architectural style for web services where resources are accessed through URLs and HTTP methods like GET, POST, PUT, PATCH, and DELETE. It is stateless and commonly used for building scalable APIs.",
        "How do you ensure application scalability?": "I focus on modular design, horizontal scaling, load balancing, caching, database optimization, and monitoring. I also separate workloads such as reads, writes, and background jobs to improve performance under load.",
        "What are JWT tokens used for?": "JWT is used for stateless authentication and authorization. It allows a server to verify a user’s identity and permissions without storing session state, which makes distributed systems easier to scale.",
        "How do you secure an API?": "I would use HTTPS, authentication, authorization, validation, rate limiting, input sanitization, and proper error handling. I would also avoid exposing sensitive information and use secure secret management.",
        "Explain caching and its benefits.": "Caching stores frequently accessed data in memory or a fast storage layer so repeated reads can be served quickly. This reduces load on the database, improves response time, and helps systems scale better.",
        "What is the difference between SQL and NoSQL?": "SQL databases use structured tables with relationships and are great for transactional systems, while NoSQL databases are more flexible for unstructured or rapidly changing data. The choice depends on the data model and workload requirements.",
        "How do you handle concurrency in a backend service?": "I would use locks, transactions, idempotent operations, and proper database isolation where required. It is also important to design for race conditions and handle retries safely in distributed systems.",
        "What is load balancing and why is it used?": "Load balancing distributes incoming traffic across multiple servers to improve performance, reliability, and availability. It prevents one server from becoming overloaded and helps maintain uptime during high traffic.",
    },
    "Data Analyst": {
        "What is the difference between inner join and left join?": "An inner join returns only rows that have matches in both tables, while a left join returns all rows from the left table and matched rows from the right table. Left joins are useful when you want to keep all records from the primary dataset.",
        "How do you clean messy data?": "I remove duplicates, standardize formats, handle missing values, validate inconsistent entries, and correct obvious errors. A clean dataset improves the accuracy of analysis and reduces misleading results.",
        "How do you handle missing values in a dataset?": "I investigate why values are missing, then apply the right strategy depending on the case, like dropping rows, filling with median/mean, or using a category label for missing values. The choice depends on the data and business context.",
        "What is normalization in a database?": "Normalization is the process of organizing data to reduce redundancy and improve integrity. It divides large tables into smaller related tables and uses keys to keep the data consistent and efficient.",
        "What is the purpose of SQL subqueries?": "Subqueries help break complex logic into smaller steps by nesting one query inside another. They are useful for filtering, aggregating, or comparing values before the final result is produced.",
        "How do you measure data quality?": "I check completeness, accuracy, consistency, uniqueness, timeliness, and validity. Good data quality ensures the results of analysis are trustworthy and actionable.",
        "Explain correlation vs causation.": "Correlation means two variables move together, while causation means one variable directly causes the other to change. It is important not to assume a cause just because two trends appear related.",
        "What is the difference between a primary key and a foreign key?": "A primary key uniquely identifies each row in a table, while a foreign key references the primary key of another table. Foreign keys help maintain relationships and data integrity between tables.",
    },
    "Full Stack Developer": {
        "How do you connect frontend to backend securely?": "I use HTTPS, proper authentication and authorization, secure token storage, and validated API requests. I also protect against common issues like XSS, CSRF, and injection attacks by validating inputs and enforcing safe patterns.",
        "Explain authentication vs authorization.": "Authentication verifies who the user is, while authorization decides what that user is allowed to do. A user can be authenticated but still lack permission to access certain resources.",
        "What is the role of a database in a full stack app?": "The database stores application data and supports retrieval, updates, and relationships between entities. It is essential for persistence, reporting, and maintaining the app’s core state reliably.",
        "How do you handle state across frontend and backend?": "I keep the backend as the source of truth for persistent data and use frontend state for UI interactions. I also use APIs, caching, and clear data flow patterns to keep both sides synchronized and predictable.",
        "What is CI/CD and why is it important?": "CI/CD automates integration and deployment, helping teams detect issues early and release faster. CI checks code quality and tests, while CD deploys tested code to environments automatically.",
        "How do you deploy a web app securely?": "I would use environment variables for secrets, secure infrastructure configuration, HTTPS, a managed platform, and monitoring. I would also maintain rollback strategies and proper access controls for deployment pipelines.",
        "How do you debug issues across frontend and backend?": "I start by reproducing the issue, checking the request flow, reviewing logs, and verifying whether data is correct at each layer. This helps isolate whether the bug is caused by the UI, API, database, or infrastructure.",
        "Explain the difference between monolithic and microservices architecture.": "A monolith is one application with tightly coupled components, while microservices split the app into smaller independent services. Microservices improve scaling and team independence, but they add operational and communication complexity.",
    },
}


def build_aptitude_questions():
    questions = [
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
    random.shuffle(questions)
    return questions[:10]


def generate_pdf_notes(role, questions, answers):
    lines = [
        "Career Prep Notes",
        f"Role: {role}",
        "",
        "Technical Interview Questions and Notes",
        "",
    ]

    for index, question in enumerate(questions, start=1):
        user_answer = answers.get(index, "Not answered")
        ideal_answer = TECHNICAL_ANSWER_GUIDES.get(role, {}).get(question, "Use a clear structure: explain the concept, give a real example, and mention trade-offs.")

        lines.append(f"Q{index}: {question}")
        lines.append(f"Your answer: {user_answer}")
        lines.append("Better answer:")
        lines.append(ideal_answer)
        lines.append("Improvement tip: Answer with a short definition, one practical example, and the trade-offs or use cases.")
        lines.append("")

    lines.append("Suggested next step: revise the weak areas, watch a relevant YouTube topic video, and answer again using a structured format.")

    text = []
    y = 760
    for line in lines:
        safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        text.append(f"BT /F1 10 Tf 72 {y} Td ({safe}) Tj ET")
        y -= 16

    content_stream = "\n".join(text).encode("latin-1", "replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        (
            b"<< /Length " + str(len(content_stream)).encode("ascii") + b" >>\nstream\n" + content_stream + b"\nendstream"
        ),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]

    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode("ascii"))
    return bytes(pdf)


def render_internship_pipeline():
    user = st.session_state.user
    db = SessionLocal()

    try:
        st.subheader("Internship Pipeline")
        st.caption("Save opportunities, apply, track outcomes, and prepare for each role.")

        with st.expander("Add internship opportunity"):
            with st.form("add_internship_form"):
                col1, col2 = st.columns(2)
                with col1:
                    company_name = st.text_input("Company")
                    role = st.text_input("Role")
                    location = st.text_input("Location", placeholder="Bengaluru or Remote")
                with col2:
                    work_mode = st.selectbox("Work mode", ["Remote", "Hybrid", "On-site"])
                    application_deadline = st.date_input("Application deadline", value=date.today())
                    application_url = st.text_input("Application URL")
                skills = st.text_input("Required skills", placeholder="Python, SQL, communication")
                description = st.text_area("Description")
                submitted = st.form_submit_button("Save internship", use_container_width=True)
                if submitted:
                    if not company_name.strip() or not role.strip():
                        st.error("Company and role are required.")
                    else:
                        create_internship(
                            db, user.id, company_name, role, description, location,
                            work_mode, skills, application_deadline, application_url,
                        )
                        st.success("Internship saved.")
                        st.rerun()

        search = st.text_input("Search by company, role, or skill", key="internship_search")
        status_filter = st.selectbox(
            "Filter status",
            ["All", "Saved", "Preparing", "Applied", "Interview", "Selected", "Rejected"],
            key="internship_status_filter",
        )
        internships = get_internships(db, user.id, search, status_filter)

        st.markdown(f"**Opportunities ({len(internships)})**")
        if not internships:
            st.info("No internships match your search. Add an opportunity above to begin.")
        else:
            internship_options = {
                f"{item.company_name} - {item.role} ({item.status})": item.id
                for item in internships
            }
            selected_label = st.selectbox("View internship", list(internship_options), key="selected_internship")
            selected_id = internship_options[selected_label]
            internship = next(item for item in internships if item.id == selected_id)

            st.markdown(f"### {internship.role} at {internship.company_name}")
            st.write(internship.description or "No description added.")
            st.write(f"**Location:** {internship.location or 'Not specified'}  |  **Mode:** {internship.work_mode or 'Not specified'}")
            st.write(f"**Skills:** {internship.skills or 'Not specified'}  |  **Deadline:** {internship.application_deadline or 'Not specified'}")
            if internship.application_url:
                st.link_button("Open application", internship.application_url)

            applications = get_applications(db, user.id)
            current_application = next((item for item in applications if item.internship_id == internship.id), None)
            if current_application is None:
                with st.form(f"apply_form_{internship.id}"):
                    notes = st.text_area("Application notes", placeholder="Resume version, referral, or submission details")
                    apply_submitted = st.form_submit_button("Apply and track application", use_container_width=True)
                    if apply_submitted:
                        apply_for_internship(db, user.id, internship.id, notes)
                        update_internship_status(db, user.id, internship.id, "Applied")
                        st.success("Application added to your tracker.")
                        st.rerun()
            else:
                st.info(f"Application status: {current_application.status} | Applied: {current_application.applied_date}")
                new_internship_status = st.selectbox(
                    "Update pipeline status",
                    ["Applied", "Preparing", "Interview", "Selected", "Rejected"],
                    index=["Applied", "Preparing", "Interview", "Selected", "Rejected"].index(internship.status) if internship.status in ["Applied", "Preparing", "Interview", "Selected", "Rejected"] else 0,
                    key=f"pipeline_status_{internship.id}",
                )
                if st.button("Save pipeline status", key=f"save_pipeline_{internship.id}"):
                    update_internship_status(db, user.id, internship.id, new_internship_status)
                    update_application(db, user.id, current_application.id, new_internship_status, current_application.interview_date, current_application.notes or "")
                    st.success("Application status updated.")
                    st.rerun()

        st.divider()
        st.subheader("Track applications")
        applications = get_applications(db, user.id)
        if not applications:
            st.info("Applications you submit will appear here.")
        for application in applications:
            internship = next((item for item in get_internships(db, user.id) if item.id == application.internship_id), None)
            if internship is None:
                continue
            with st.expander(f"{internship.company_name} - {internship.role} | {application.status}"):
                st.write(f"Applied on {application.applied_date}")
                with st.form(f"application_update_{application.id}"):
                    status = st.selectbox("Status", ["Applied", "Shortlisted", "Interview", "Selected", "Rejected"], index=["Applied", "Shortlisted", "Interview", "Selected", "Rejected"].index(application.status) if application.status in ["Applied", "Shortlisted", "Interview", "Selected", "Rejected"] else 0)
                    interview_date = st.date_input("Interview date", value=application.interview_date or date.today())
                    notes = st.text_area("Notes", value=application.notes or "")
                    saved = st.form_submit_button("Update application")
                    if saved:
                        update_application(db, user.id, application.id, status, interview_date, notes)
                        update_internship_status(db, user.id, internship.id, status if status != "Shortlisted" else "Interview")
                        st.success("Application tracker updated.")
                        st.rerun()

        st.divider()
        st.subheader("Track preparation")
        all_internships = get_internships(db, user.id)
        if all_internships:
            prep_options = {f"{item.company_name} - {item.role}": item.id for item in all_internships}
            prep_label = st.selectbox("Preparation target", list(prep_options), key="prep_target")
            prep_internship_id = prep_options[prep_label]
            with st.form("add_preparation_form"):
                col1, col2 = st.columns(2)
                with col1:
                    title = st.text_input("Preparation task", placeholder="Practice REST API questions")
                    category = st.selectbox("Category", ["Technical", "DSA", "SQL", "Aptitude", "HR", "Interview"])
                    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                with col2:
                    duration = st.number_input("Duration (minutes)", min_value=5, max_value=600, value=30, step=5)
                    preparation_date = st.date_input("Preparation date", value=date.today())
                description = st.text_area("Task details")
                prep_submitted = st.form_submit_button("Add preparation task", use_container_width=True)
                if prep_submitted:
                    if not title.strip():
                        st.error("A preparation task title is required.")
                    else:
                        create_preparation_task(db, user.id, prep_internship_id, title, description, category, priority, duration, preparation_date)
                        task_text = f"{title} {category}".lower()
                        if "dsa" in task_text and "array" in task_text:
                            create_preparation_task(
                                db,
                                user.id,
                                prep_internship_id,
                                "Watch YouTube lesson for array DSA",
                                "Review array patterns and solutions before attempting the problem list.",
                                "Video",
                                "Low",
                                45,
                                preparation_date,
                            )
                        st.success("Preparation task added.")
                        st.rerun()

            preparation_tasks = get_preparation_tasks(db, user.id, prep_internship_id)
            completed_count = sum(task.completed for task in preparation_tasks)
            st.progress(completed_count / len(preparation_tasks) if preparation_tasks else 0, text=f"Preparation progress: {completed_count}/{len(preparation_tasks)} complete")
            for task in preparation_tasks:
                checked = st.checkbox(
                    f"{task.title} | {task.category or 'General'} | {task.preparation_date or 'Unscheduled'}",
                    value=task.completed,
                    key=f"prep_task_{task.id}",
                )
                if checked != task.completed:
                    set_preparation_completed(db, user.id, task.id, checked)
                    st.rerun()
                if task.description:
                    st.caption(task.description)
                resources = get_task_resources(task)
                if resources:
                    st.markdown("**Study resources**")
                    st.markdown(f"[Open YouTube lesson]({resources['youtube']})")
                    for index, (problem, url) in enumerate(resources["problems"], start=1):
                        st.markdown(f"{index}. [{problem}]({url})")
        else:
            st.info("Save an internship before creating preparation tasks.")
    finally:
        db.close()


def render_career():
    st.title("Career Prep Hub")
    st.caption("Smart learning space for placement prep, interview practice, and skill-building for freshers and students.")

    render_internship_pipeline()

    st.divider()
    st.subheader("Interview preparation")

    st.subheader("Choose your preparation track")
    selected_role = st.selectbox(
        "Target role",
        ["Software Engineer", "Frontend Developer", "Backend Developer", "Data Analyst", "Full Stack Developer"],
    )

    st.markdown("### YouTube learning links")
    for item in ROLE_LEARNING_LINKS.get(selected_role, ROLE_LEARNING_LINKS["Software Engineer"]):
        with st.container():
            st.markdown(f"#### {item['title']}")
            st.write(item["description"])
            st.markdown(f"[▶ Open YouTube learning link]({item['url']})")

    st.divider()

    st.subheader("Aptitude Test")
    if "aptitude_started" not in st.session_state:
        st.session_state.aptitude_started = False
        st.session_state.aptitude_index = 0
        st.session_state.aptitude_answers = {}
        st.session_state.aptitude_time = 600
        st.session_state.aptitude_questions = build_aptitude_questions()
        st.session_state.aptitude_start_time = time.time()

    if not st.session_state.aptitude_started:
        if st.button("Start Aptitude Exam"):
            st.session_state.aptitude_started = True
            st.session_state.aptitude_start_time = time.time()
            st.session_state.aptitude_questions = build_aptitude_questions()
            st.session_state.aptitude_index = 0
            st.session_state.aptitude_answers = {}
            st.rerun()
    else:
        elapsed = int(time.time() - st.session_state.aptitude_start_time)
        remaining = max(0, st.session_state.aptitude_time - elapsed)
        minutes, seconds = divmod(remaining, 60)
        st.info(f"⏱️ Time Remaining: {minutes:02d}:{seconds:02d}")

        if remaining <= 0:
            st.warning("Time is up! Your aptitude exam has ended.")
            final_score = 0
            for idx, item in enumerate(st.session_state.aptitude_questions):
                if st.session_state.aptitude_answers.get(idx) == item["answer"]:
                    final_score += 1
            st.success(f"🏁 Final score: {final_score}/{len(st.session_state.aptitude_questions)}")
            st.session_state.aptitude_started = False
            st.session_state.aptitude_index = 0
            st.session_state.aptitude_answers = {}
            st.session_state.aptitude_questions = build_aptitude_questions()
            st.stop()

        q_index = st.session_state.aptitude_index
        q = st.session_state.aptitude_questions[q_index]

        st.write(f"**Question {q_index + 1}/{len(st.session_state.aptitude_questions)}**")
        st.write(q["question"])

        selected = st.radio("Choose the correct answer", q["options"], index=None, key=f"aptitude_{q_index}", horizontal=True)
        if selected is not None:
            st.session_state.aptitude_answers[q_index] = selected

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Next Question"):
                if st.session_state.aptitude_index < len(st.session_state.aptitude_questions) - 1:
                    st.session_state.aptitude_index += 1
                    st.rerun()
                else:
                    final_score = 0
                    for idx, item in enumerate(st.session_state.aptitude_questions):
                        if st.session_state.aptitude_answers.get(idx) == item["answer"]:
                            final_score += 1
                    st.success(f"Aptitude test complete! Final score: {final_score}/{len(st.session_state.aptitude_questions)}")
                    st.session_state.aptitude_started = False
                    st.session_state.aptitude_index = 0
                    st.session_state.aptitude_answers = {}
                    st.session_state.aptitude_questions = build_aptitude_questions()
                    st.stop()

        with col2:
            if st.button("Reset Exam"):
                st.session_state.aptitude_started = False
                st.session_state.aptitude_index = 0
                st.session_state.aptitude_answers = {}
                st.session_state.aptitude_questions = build_aptitude_questions()
                st.rerun()

    st.divider()

    st.subheader("Technical Interview Drill")
    tech_role = st.selectbox("Choose technical focus", ["Software Engineer", "Frontend Developer", "Backend Developer", "Data Analyst", "Full Stack Developer"])
    bank = {
        "Software Engineer": [
            "What is the difference between a process and a thread?",
            "Explain OOP concepts in your own words.",
            "How do you optimize a slow SQL query?",
            "What is the difference between GET and POST?",
            "How do you debug a production bug?",
            "Explain database indexing and why it matters.",
            "How do you design a scalable backend system?",
            "What is the difference between synchronous and asynchronous programming?",
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
        "Data Analyst": [
            "What is the difference between inner join and left join?",
            "How do you clean messy data?",
            "How do you handle missing values in a dataset?",
            "What is normalization in a database?",
            "What is the purpose of SQL subqueries?",
            "How do you measure data quality?",
            "Explain correlation vs causation.",
            "What is the difference between a primary key and a foreign key?",
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

    if "tech_round_started" not in st.session_state:
        st.session_state.tech_round_started = False
        st.session_state.tech_questions = []
        st.session_state.tech_answers = {}
        st.session_state.tech_index = 0

    if not st.session_state.tech_round_started:
        if st.button("Start Technical Questions"):
            st.session_state.tech_round_started = True
            st.session_state.tech_questions = random.sample(bank[tech_role], 3)
            st.session_state.tech_answers = {}
            st.session_state.tech_index = 0
            st.rerun()
    else:
        if st.session_state.tech_index < len(st.session_state.tech_questions):
            q = st.session_state.tech_questions[st.session_state.tech_index]
            st.markdown(f"### Question {st.session_state.tech_index + 1}")
            st.write(q)
            answer = st.text_area(
                "Your answer",
                key=f"tech_answer_{st.session_state.tech_index}",
                height=120,
                label_visibility="collapsed",
            )

            if st.button("Save and Next"):
                st.session_state.tech_answers[st.session_state.tech_index + 1] = answer.strip()
                if st.session_state.tech_index < len(st.session_state.tech_questions) - 1:
                    st.session_state.tech_index += 1
                    st.rerun()
                else:
                    st.session_state.tech_round_started = False
                    st.success("Technical questions completed. Download your notes below.")
                    st.download_button(
                        label="Download PDF notes",
                        data=generate_pdf_notes(tech_role, st.session_state.tech_questions, st.session_state.tech_answers),
                        file_name=f"{tech_role.lower().replace(' ', '_')}_notes.pdf",
                        mime="application/pdf",
                    )
                    st.stop()
        else:
            st.success("Technical questions completed. Download your notes below.")
            st.download_button(
                label="Download PDF notes",
                data=generate_pdf_notes(tech_role, st.session_state.tech_questions, st.session_state.tech_answers),
                file_name=f"{tech_role.lower().replace(' ', '_')}_notes.pdf",
                mime="application/pdf",
            )

    st.divider()

    st.subheader("📌 Daily productivity plan")
    st.markdown(
        """
        - 20 minutes aptitude practice
        - 20 minutes technical concept revision
        - 30 minutes project or coding work
        - 10 minutes resume and interview reflection
        """
    )
    st.success("This section gives you direct learning links, randomized test practice, and a ready-made PDF note pack for interview preparation.")
