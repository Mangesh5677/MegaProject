
import streamlit as st
import pandas as pd

from datetime import date, datetime, time, timedelta

from modules.database.database import SessionLocal
from modules.database.models import User
from modules.database.activity import UserActivity
from modules.database.crud import (
    assign_task_to_user,
    delete_user_account,
    get_admin_assigned_tasks,
)

from modules.analytics.activity_service import (
    get_admin_user_stats,
    get_recent_activities,
)


def render_admin_dashboard():

    # ==========================================
    # 1. Verify admin access
    # ==========================================
    user = st.session_state.get("user")

    if user is None:
        st.error("Please log in first.")
        st.stop()

    if getattr(user, "role", "user") != "admin":
        st.error("Access denied. Admin privileges required.")
        st.stop()

    # ==========================================
    # 2. Dashboard header
    # ==========================================
    st.title("🛡️ Advanced Admin Analytics")
    st.caption(
        "Monitor registered users, feature usage, "
        "productivity, and application activity."
    )

    deleted_user_name = st.session_state.pop(
        "admin_deleted_user_name",
        None,
    )
    if deleted_user_name:
        st.success(f"Deleted account for {deleted_user_name}.")

    # ==========================================
    # 3. Date filter
    # ==========================================
    st.subheader("📅 Analytics Date Range")

    period = st.selectbox(
        "Select reporting period",
        ["Last 7 Days", "Last 30 Days", "Custom Range"],
        index=1,
    )

    today = date.today()

    if period == "Last 7 Days":
        start_date = today - timedelta(days=6)
        end_date = today

    elif period == "Last 30 Days":
        start_date = today - timedelta(days=29)
        end_date = today

    else:
        col_start, col_end = st.columns(2)

        with col_start:
            start_date = st.date_input(
                "Start date",
                value=today - timedelta(days=29),
                max_value=today,
                key="admin_analytics_start",
            )

        with col_end:
            end_date = st.date_input(
                "End date",
                value=today,
                max_value=today,
                key="admin_analytics_end",
            )

        if start_date > end_date:
            st.error("Start date must not be after end date.")
            st.stop()

    start_datetime = datetime.combine(
        start_date, time.min
    )
    end_datetime = datetime.combine(
        end_date, time.max
    )

    # ==========================================
    # 4. Load data
    # ==========================================
    db = SessionLocal()

    try:
        stats = get_admin_user_stats(db)

        # Activities inside selected date range
        activities = (
            db.query(UserActivity, User)
            .join(User, User.id == UserActivity.user_id)
            .filter(
                UserActivity.created_at >= start_datetime,
                UserActivity.created_at <= end_datetime,
            )
            .order_by(UserActivity.created_at.desc())
            .all()
        )

        # All-time registered users
        total_users = db.query(User).count()
        assignable_users = (
            db.query(User)
            .filter(User.role == "user")
            .order_by(User.name)
            .all()
        )

        # ======================================
        # 5. All-time platform overview
        # ======================================
        st.subheader("📊 Platform Overview")
        st.caption(
            "These summary metrics cover all recorded history."
        )

        total_logins = sum(
            item["total_logins"] for item in stats
        )
        total_chatbot = sum(
            item["chatbot_uses"] for item in stats
        )
        total_scheduler = sum(
            item["scheduler_uses"] for item in stats
        )
        total_created = sum(
            item["tasks_created"] for item in stats
        )
        total_completed = sum(
            item["tasks_completed"] for item in stats
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Registered Users", total_users)
        c2.metric("Total Logins", total_logins)
        c3.metric("Chatbot Uses", total_chatbot)

        c4, c5, c6 = st.columns(3)
        c4.metric("AI Scheduler Uses", total_scheduler)
        c5.metric("Tasks Created", total_created)
        c6.metric("Tasks Completed", total_completed)

        st.divider()
        st.subheader("📝 Assign a Task")
        st.caption(
            "Assign a one-time task to a regular user. "
            "The task and deadline will appear in their task list."
        )

        if not assignable_users:
            st.info("There are no regular user accounts to assign tasks to.")
        else:
            user_labels = {
                assigned_user.id: (
                    f"{assigned_user.name} ({assigned_user.email})"
                )
                for assigned_user in assignable_users
            }

            with st.form("admin_assign_task_form"):
                assigned_user_id = st.selectbox(
                    "Assign to",
                    options=list(user_labels),
                    format_func=user_labels.get,
                    key="admin_assign_task_user",
                )
                task_title = st.text_input(
                    "Task title",
                    placeholder="Example: Submit the project report",
                    key="admin_assign_task_title",
                )
                task_description = st.text_area(
                    "Description",
                    placeholder="Add instructions or details for the user.",
                    key="admin_assign_task_description",
                )

                task_col1, task_col2 = st.columns(2)
                with task_col1:
                    task_priority = st.selectbox(
                        "Priority",
                        ["Low", "Medium", "High"],
                        key="admin_assign_task_priority",
                    )
                    task_due_date = st.date_input(
                        "Deadline date",
                        value=today,
                        key="admin_assign_task_due_date",
                    )
                with task_col2:
                    task_duration = st.number_input(
                        "Estimated duration (minutes)",
                        min_value=15,
                        max_value=600,
                        value=60,
                        step=15,
                        key="admin_assign_task_duration",
                    )
                    task_due_time = st.time_input(
                        "Deadline time",
                        value=time(18, 0),
                        key="admin_assign_task_due_time",
                    )

                assign_submitted = st.form_submit_button(
                    "Assign task",
                    use_container_width=True,
                )

            if assign_submitted:
                if not task_title.strip():
                    st.error("Enter a title for the task.")
                else:
                    try:
                        assign_task_to_user(
                            db=db,
                            admin_id=user.id,
                            user_id=assigned_user_id,
                            title=task_title.strip(),
                            description=task_description.strip(),
                            priority=task_priority,
                            due_date=task_due_date,
                            due_time=task_due_time,
                            duration=task_duration,
                        )
                    except (PermissionError, ValueError) as error:
                        st.error(str(error))
                    else:
                        st.success(
                            f"Task assigned to "
                            f"{user_labels[assigned_user_id]}."
                        )
                        st.rerun()

        assigned_tasks = get_admin_assigned_tasks(db, user.id)
        st.markdown("#### Assigned task progress")
        if not assigned_tasks:
            st.info("You have not assigned any tasks yet.")
        else:
            assigned_task_rows = [
                {
                    "Task": task.title,
                    "Assigned to": assignee.name,
                    "Email": assignee.email,
                    "Deadline": (
                        f"{task.due_date or 'No date'}"
                        f" {task.due_time.strftime('%I:%M %p') if task.due_time else ''}"
                    ).strip(),
                    "Priority": task.priority or "—",
                    "Status": task.status or "Pending",
                }
                for task, assignee in assigned_tasks
            ]
            assigned_tasks_df = pd.DataFrame(assigned_task_rows)
            total_assigned = len(assigned_task_rows)
            total_assigned_completed = sum(
                task.status == "Completed"
                for task, _ in assigned_tasks
            )
            progress_col1, progress_col2, progress_col3 = st.columns(3)
            progress_col1.metric("Assigned", total_assigned)
            progress_col2.metric("Completed", total_assigned_completed)
            progress_col3.metric(
                "Pending",
                total_assigned - total_assigned_completed,
            )
            st.dataframe(
                assigned_tasks_df,
                use_container_width=True,
                hide_index=True,
            )

        st.divider()

        # ======================================
        # 6. Prepare filtered activity data
        # ======================================
        activity_rows = []

        for activity, activity_user in activities:
            activity_rows.append({
                "User": activity_user.name,
                "Email": activity_user.email,
                "Activity": activity.activity_type,
                "Details": activity.activity_details or "",
                "Date & Time": activity.created_at,
            })

        activity_df = pd.DataFrame(
            activity_rows,
            columns=[
                "User",
                "Email",
                "Activity",
                "Details",
                "Date & Time",
            ],
        )

        st.subheader("📈 Activity Analytics")
        st.caption(
            f"Showing recorded activity from "
            f"{start_date:%d %b %Y} to {end_date:%d %b %Y}."
        )

        if activity_df.empty:
            st.info(
                "No activity was recorded during this period. "
                "Try another date range."
            )
        else:
            activity_df["Date & Time"] = pd.to_datetime(
                activity_df["Date & Time"]
            )
            activity_df["Date"] = (
                activity_df["Date & Time"].dt.date
            )

            # ----------------------------------
            # Daily activity trend
            # ----------------------------------
            st.markdown("#### 📊 Daily Activity Trend")

            daily_activity = (
                activity_df.groupby("Date")
                .size()
                .rename("Activities")
            )

            all_dates = pd.date_range(
                start=start_date,
                end=end_date,
                freq="D",
            ).date

            daily_activity = daily_activity.reindex(
                all_dates,
                fill_value=0,
            )

            daily_activity.index = pd.to_datetime(
                daily_activity.index
            )

            st.line_chart(
                daily_activity,
                use_container_width=True,
            )

            # ----------------------------------
            # Feature usage chart
            # ----------------------------------
            st.markdown("#### 🤖 Feature Usage")

            feature_labels = {
                "LOGIN": "Logins",
                "AI_CHAT": "Chatbot",
                "AI_SCHEDULER": "AI Scheduler",
                "TASK_CREATED": "Tasks Created",
                "TASK_ASSIGNED": "Tasks Assigned",
                "TASK_COMPLETED": "Tasks Completed",
            }

            feature_activity = (
                activity_df["Activity"]
                .map(feature_labels)
                .fillna("Other Activities")
                .value_counts()
                .rename_axis("Feature")
                .to_frame("Uses")
            )

            st.bar_chart(
                feature_activity,
                use_container_width=True,
            )

            # ----------------------------------
            # Daily feature trends
            # ----------------------------------
            st.markdown("#### 📉 Daily Feature Trends")

            tracked_types = [
                "LOGIN",
                "AI_CHAT",
                "AI_SCHEDULER",
                "TASK_CREATED",
                "TASK_ASSIGNED",
                "TASK_COMPLETED",
            ]

            daily_features = (
                activity_df[
                    activity_df["Activity"].isin(tracked_types)
                ]
                .groupby([
                    "Date",
                    "Activity",
                ])
                .size()
                .unstack(fill_value=0)
            )

            daily_features.index = pd.to_datetime(
                daily_features.index
            )

            full_dates = pd.date_range(
                start=start_date,
                end=end_date,
                freq="D",
            )

            daily_features = daily_features.reindex(
                full_dates,
                fill_value=0,
            )

            daily_features.index.name = "Date"

            if not daily_features.empty:
                st.line_chart(
                    daily_features,
                    use_container_width=True,
                )
            else:
                st.info("No tracked feature activity found.")

        # ======================================
        # 7. User registration trend
        # ======================================
        st.divider()
        st.subheader("👥 User Registration Trends")

        registrations = (
            db.query(User)
            .filter(
                User.created_at >= start_datetime,
                User.created_at <= end_datetime,
            )
            .all()
        )

        if registrations:
            registration_df = pd.DataFrame([
                {
                    "Date": pd.to_datetime(
                        registered_user.created_at
                    ).date(),
                }
                for registered_user in registrations
            ])

            registration_counts = (
                registration_df.groupby("Date")
                .size()
                .rename("New Registrations")
            )
        else:
            registration_counts = pd.Series(
                dtype="int64",
                name="New Registrations",
            )

        registration_dates = pd.date_range(
            start=start_date,
            end=end_date,
            freq="D",
        ).date

        registration_counts = registration_counts.reindex(
            registration_dates,
            fill_value=0,
        )

        registration_counts.index = pd.to_datetime(
            registration_counts.index
        )

        st.bar_chart(
            registration_counts,
            use_container_width=True,
        )

        # ======================================
        # 8. Registered users management
        # ======================================
        st.divider()
        st.subheader("👥 Registered Users Management")

        if stats:
            users_df = pd.DataFrame([
                {
                    "ID": item["id"],
                    "Name": item["name"],
                    "Email": item["email"],
                    "Role": item["role"],
                    "Registered At": item["registered_at"],
                    "Logins": item["total_logins"],
                    "Chatbot Uses": item["chatbot_uses"],
                    "Scheduler Uses": item["scheduler_uses"],
                    "Tasks Created": item["tasks_created"],
                    "Tasks Completed": item["tasks_completed"],
                    "Total Activities": item["total_activities"],
                }
                for item in stats
            ])

            # Search users
            search = st.text_input(
                "🔍 Search by name or email",
                placeholder="Enter a name or email...",
                key="admin_user_search",
            )

            # Role filter
            roles = ["All", "admin", "user"]
            selected_role = st.selectbox(
                "Filter by role",
                roles,
                key="admin_role_filter",
            )

            # Registration date filter
            users_df["Registered At"] = pd.to_datetime(
                users_df["Registered At"],
                errors="coerce",
            )

            valid_dates = users_df["Registered At"].dropna()

            if not valid_dates.empty:
                min_date = valid_dates.min().date()
                max_date = valid_dates.max().date()

                date_filter = st.checkbox(
                    "Filter by registration date",
                    key="admin_registration_date_filter",
                )

                if date_filter:
                    date_col1, date_col2 = st.columns(2)

                    with date_col1:
                        registration_start = st.date_input(
                            "Registered from",
                            value=min_date,
                            min_value=min_date,
                            max_value=max_date,
                            key="admin_registration_start",
                        )

                    with date_col2:
                        registration_end = st.date_input(
                            "Registered until",
                            value=max_date,
                            min_value=min_date,
                            max_value=max_date,
                            key="admin_registration_end",
                        )

                    if registration_start > registration_end:
                        st.error(
                            "Start date cannot be after end date."
                        )
                        st.stop()

            filtered_df = users_df.copy()

            # Apply search
            if search.strip():
                search_text = search.strip()

                matches = (
                    filtered_df["Name"].astype(str).str.contains(
                        search_text,
                        case=False,
                        na=False,
                        regex=False,
                    )
                    |
                    filtered_df["Email"].astype(str).str.contains(
                        search_text,
                        case=False,
                        na=False,
                        regex=False,
                    )
                )

                filtered_df = filtered_df[matches]

            # Apply role filter
            if selected_role != "All":
                filtered_df = filtered_df[
                    filtered_df["Role"] == selected_role
                ]

            # Apply registration date filter
            if (
                valid_dates.size > 0
                and st.session_state.get(
                    "admin_registration_date_filter",
                    False,
                )
            ):
                filtered_df = filtered_df[
                    (
                        filtered_df["Registered At"].dt.date
                        >= registration_start
                    )
                    &
                    (
                        filtered_df["Registered At"].dt.date
                        <= registration_end
                    )
                ]

            st.caption(
                f"Showing {len(filtered_df)} of "
                f"{len(users_df)} registered users."
            )

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "⬇️ Export Filtered Users (CSV)",
                data=filtered_df.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="filtered_user_report.csv",
                mime="text/csv",
                key="export_filtered_users",
            )

            user_accounts = users_df.loc[
                users_df["Role"] == "user",
                ["ID", "Name", "Email"],
            ]

            if not user_accounts.empty:
                account_labels = {
                    int(row["ID"]): f'{row["Name"]} ({row["Email"]})'
                    for _, row in user_accounts.iterrows()
                }

                st.markdown("#### Manage user accounts")
                st.warning(
                    "Deleting an account permanently removes its tasks, "
                    "schedules, career records, rewards, and activity history."
                )

                with st.form("admin_delete_user_form"):
                    selected_user_id = st.selectbox(
                        "Select a user account",
                        options=list(account_labels),
                        format_func=account_labels.get,
                        key="admin_delete_user_id",
                    )
                    confirmed = st.checkbox(
                        "I understand this permanently deletes the account and its data.",
                        key="admin_delete_user_confirm",
                    )
                    delete_submitted = st.form_submit_button(
                        "Delete user account"
                    )

                if delete_submitted:
                    if not confirmed:
                        st.error("Confirm the deletion before continuing.")
                    else:
                        try:
                            deleted = delete_user_account(
                                db,
                                selected_user_id,
                            )
                        except Exception:
                            st.error(
                                "The account could not be deleted. "
                                "Please try again."
                            )
                        else:
                            if deleted:
                                st.session_state[
                                    "admin_deleted_user_name"
                                ] = account_labels[selected_user_id]
                                st.rerun()

                            st.error(
                                "Only regular user accounts can be deleted."
                            )

        else:
            st.info("No registered users found.")
        # ======================================
        # 9. Filtered activity history
        # ======================================
        st.divider()
        st.subheader("🕒 Activity History")

        if not activity_df.empty:
            display_df = activity_df.drop(
                columns=["Date"]
                if "Date" in activity_df.columns
                else [],
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "⬇️ Export Filtered Activity (CSV)",
                data=display_df.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="filtered_activity_report.csv",
                mime="text/csv",
            )
        else:
            st.info(
                "No activity records found for the selected period."
            )

        st.caption(
            "Analytics use recorded application events and "
            "registration timestamps. Missing historical events "
            "cannot be reconstructed."
        )

    finally:
        db.close()