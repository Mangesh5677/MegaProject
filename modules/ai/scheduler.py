from datetime import datetime, timedelta, time

from modules.database.models import Task, FixedSchedule


# ============================================================
# Helper: Check whether a time slot overlaps fixed timetable
# ============================================================

def is_time_available(
    start_time,
    end_time,
    fixed_schedules
):
    for schedule in fixed_schedules:

        fixed_start = schedule.start_time
        fixed_end = schedule.end_time

        if not fixed_start or not fixed_end:
            continue

        # Overlap check
        if (
            start_time < fixed_end
            and end_time > fixed_start
        ):
            return False

    return True


# ============================================================
# Generate AI Schedule
# ============================================================

def generate_schedule(db, user_id):

    # ========================================================
    # Get ONLY logged-in user's pending tasks
    # ========================================================

    tasks = (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .filter(Task.status == "Pending")
        .order_by(Task.due_date, Task.priority)
        .all()
    )

    # ========================================================
    # Get ONLY logged-in user's fixed timetable
    # ========================================================

    fixed_schedules = (
        db.query(FixedSchedule)
        .filter(FixedSchedule.user_id == user_id)
        .all()
    )

    scheduled = []
    unscheduled = []

    # ========================================================
    # Priority order
    # ========================================================

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    tasks.sort(
        key=lambda task: (
            priority_order.get(
                task.priority,
                3
            ),
            task.due_date or datetime.max.date()
        )
    )

    # ========================================================
    # Schedule each task
    # ========================================================

    for task in tasks:

        if not task.duration:
            task.duration = 60

        if not task.due_date:
            task.due_date = datetime.now().date()

        task_scheduled = False

        current_date = datetime.now().date()

        # Don't schedule before today
        if current_date > task.due_date:
            current_date = task.due_date

        # ====================================================
        # Search each day until deadline
        # ====================================================

        while current_date <= task.due_date:

            day_name = current_date.strftime("%A")

            # Get fixed timetable for this user's day
            day_schedule = [
                schedule
                for schedule in fixed_schedules
                if schedule.day == day_name
            ]

            # =================================================
            # Available working time
            # =================================================

            work_start = time(8, 0)
            work_end = time(22, 0)

            current_minutes = (
                work_start.hour * 60
                + work_start.minute
            )

            end_minutes = (
                work_end.hour * 60
                + work_end.minute
            )

            # =================================================
            # Try 30-minute intervals
            # =================================================

            while current_minutes + task.duration <= end_minutes:

                start_hour = current_minutes // 60
                start_minute = current_minutes % 60

                start = time(
                    start_hour,
                    start_minute
                )

                end_datetime = (
                    datetime.combine(
                        current_date,
                        start
                    )
                    + timedelta(
                        minutes=task.duration
                    )
                )

                end = end_datetime.time()

                # Don't go beyond working hours
                if end > work_end:
                    break

                # Check fixed timetable
                available = is_time_available(
                    start,
                    end,
                    day_schedule
                )

                if available:

                    # =========================================
                    # Save AI-generated schedule
                    # =========================================

                    task.scheduled_date = current_date
                    task.scheduled_start = start
                    task.scheduled_end = end

                    db.commit()
                    db.refresh(task)

                    scheduled.append(task)

                    task_scheduled = True

                    break

                current_minutes += 30

            if task_scheduled:
                break

            current_date += timedelta(days=1)

        # ====================================================
        # Couldn't schedule task
        # ====================================================

        if not task_scheduled:

            unscheduled.append(task)

    return scheduled, unscheduled