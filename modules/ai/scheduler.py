from datetime import datetime, date, time, timedelta

from modules.database.models import Task, FixedSchedule, Settings


# ============================================================
# Priority Order
# ============================================================

PRIORITY_ORDER = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}


# ============================================================
# Generate AI Schedule
# ============================================================

def generate_schedule(db, user_id):

    # --------------------------------------------------------
    # Get ONLY current user's pending tasks
    # --------------------------------------------------------

    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status == "Pending"
        )
        .all()
    )

    # --------------------------------------------------------
    # Get ONLY current user's timetable
    # --------------------------------------------------------

    timetable = (
        db.query(FixedSchedule)
        .filter(
            FixedSchedule.user_id == user_id
        )
        .all()
    )

    settings = (
        db.query(Settings)
        .filter(Settings.user_id == user_id)
        .first()
    )

    work_start = settings.work_start if settings and settings.work_start else time(8, 0)
    work_end = settings.work_end if settings and settings.work_end else time(18, 0)
    if work_start >= work_end:
        work_start = time(8, 0)
        work_end = time(18, 0)

    # --------------------------------------------------------
    # Sort by Priority + Deadline
    # --------------------------------------------------------

    tasks.sort(
        key=lambda x: (
            PRIORITY_ORDER.get(x.priority, 3),
            x.due_date or date.max
        )
    )

    scheduled = []
    unscheduled = []

    today = date.today()
    now = datetime.now()

    # --------------------------------------------------------
    # Clear previous schedule
    # --------------------------------------------------------

    for task in tasks:

        task.scheduled_date = None
        task.scheduled_start = None
        task.scheduled_end = None

    db.commit()

    # --------------------------------------------------------
    # Schedule each task
    # --------------------------------------------------------

    for task in tasks:

        duration = task.duration or 60

        found_slot = False

        current_date = today

        deadline = task.due_date or (today + timedelta(days=7))

        # If the task is already overdue, keep scheduling it on future days
        # instead of stopping at the passed deadline.
        if deadline < today:
            deadline = today + timedelta(days=30)

        while current_date <= deadline:

            day_name = current_date.strftime("%A")

            current_dt = datetime.combine(
                current_date,
                work_start
            )

            limit_dt = datetime.combine(
                current_date,
                work_end
            )

            if current_date == today:
                candidate_now = now.replace(second=0, microsecond=0)
                current_dt = max(current_dt, candidate_now)

            if current_date == today and current_dt >= limit_dt:
                current_date += timedelta(days=1)
                continue

            while current_dt + timedelta(minutes=duration) <= limit_dt:

                slot_start = current_dt.time()
                slot_end = (current_dt + timedelta(minutes=duration)).time()

                conflict = False

                for item in timetable:
                    if item.day != day_name:
                        continue
                    if slot_start < item.end_time and slot_end > item.start_time:
                        conflict = True
                        break

                if not conflict:
                    existing_tasks = (
                        db.query(Task)
                        .filter(
                            Task.user_id == user_id,
                            Task.scheduled_date == current_date
                        )
                        .all()
                    )

                    for existing in existing_tasks:
                        if existing.scheduled_start is None or existing.scheduled_end is None:
                            continue
                        if existing.id == task.id:
                            continue
                        if slot_start < existing.scheduled_end and slot_end > existing.scheduled_start:
                            conflict = True
                            break

                if conflict:
                    current_dt += timedelta(minutes=30)
                    continue

                task.scheduled_date = current_date
                task.scheduled_start = slot_start
                task.scheduled_end = slot_end

                db.commit()
                scheduled.append(task)
                found_slot = True
                break

            if found_slot:
                break

            current_date += timedelta(days=1)

            if task.task_type == "Daily / Running" and current_date > deadline:
                break

            continue

            while current_dt + timedelta(minutes=duration) <= limit_dt:

                slot_start = current_dt.time()

                slot_end = (
                    current_dt +
                    timedelta(minutes=duration)
                ).time()

                conflict = False

                # ------------------------------------------------
                # Check timetable conflicts
                # ------------------------------------------------

                for item in timetable:

                    if item.day != day_name:
                        continue

                    if (
                        slot_start < item.end_time
                        and slot_end > item.start_time
                    ):
                        conflict = True
                        break

                # ------------------------------------------------
                # Check already scheduled task conflicts
                # ------------------------------------------------

                if not conflict:

                    existing_tasks = (
                        db.query(Task)
                        .filter(
                            Task.user_id == user_id,
                            Task.scheduled_date == current_date
                        )
                        .all()
                    )

                    for existing in existing_tasks:

                        if (
                            existing.scheduled_start is None
                            or existing.scheduled_end is None
                        ):
                            continue

                        if existing.id == task.id:
                            continue

                        if (
                            slot_start < existing.scheduled_end
                            and slot_end > existing.scheduled_start
                        ):
                            conflict = True
                            break

                # ------------------------------------------------
                # Free slot found
                # ------------------------------------------------

                if not conflict:

                    task.scheduled_date = current_date
                    task.scheduled_start = slot_start
                    task.scheduled_end = slot_end

                    db.commit()

                    scheduled.append(task)

                    found_slot = True

                    break

                current_dt += timedelta(minutes=30)

            if found_slot:
                break

            current_date += timedelta(days=1)

        if not found_slot:

            unscheduled.append(task)

    db.commit()

    return scheduled, unscheduled