from .models import FixedSchedule, Task, ScheduledTask


# ============================================================
# FIXED SCHEDULE CRUD
# ============================================================

def add_fixed_schedule(
    db,
    user_id,
    day,
    title,
    category,
    start_time,
    end_time,
):
    event = FixedSchedule(
        user_id=user_id,
        day=day,
        title=title,
        category=category,
        start_time=start_time,
        end_time=end_time,
        locked=True,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def get_fixed_schedules(db, user_id):

    return (
        db.query(FixedSchedule)
        .filter(
            FixedSchedule.user_id == user_id
        )
        .order_by(
            FixedSchedule.day,
            FixedSchedule.start_time
        )
        .all()
    )


def delete_fixed_schedule(
    db,
    user_id,
    schedule_id,
):

    event = (
        db.query(FixedSchedule)
        .filter(
            FixedSchedule.id == schedule_id,
            FixedSchedule.user_id == user_id,
        )
        .first()
    )

    if event:

        db.delete(event)
        db.commit()

        return True

    return False


# ============================================================
# TASK CRUD
# ============================================================

def add_task(
    db,
    user_id,
    title,
    description,
    priority,
    due_date,
    due_time,
    duration,
    email,
    task_type="Once",
):

    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        due_time=due_time,
        duration=duration,
        email=email,
        task_type=task_type,

        reminder_24h_sent=False,
        reminder_2h_sent=False,
        reminder_30m_sent=False,

        status="Pending",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(db, user_id):

    return (
        db.query(Task)
        .filter(
            Task.user_id == user_id
        )
        .order_by(
            Task.due_date,
            Task.due_time
        )
        .all()
    )


def get_pending_tasks(db, user_id):

    return (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status == "Pending",
        )
        .order_by(
            Task.due_date,
            Task.due_time
        )
        .all()
    )


def get_completed_tasks(db, user_id):

    return (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status == "Completed",
        )
        .order_by(
            Task.due_date,
            Task.due_time
        )
        .all()
    )


def get_task_by_id(
    db,
    user_id,
    task_id,
):

    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        .first()
    )


def delete_task(
    db,
    user_id,
    task_id,
):

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        .first()
    )

    if task:

        db.delete(task)
        db.commit()

        return True

    return False


def complete_task(
    db,
    user_id,
    task_id,
):

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        .first()
    )

    if task:

        task.status = "Completed"

        db.commit()
        db.refresh(task)

        return task

    return None


def reopen_task(
    db,
    user_id,
    task_id,
):

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        .first()
    )

    if task:

        task.status = "Pending"

        db.commit()
        db.refresh(task)

        return task

    return None


# ============================================================
# AI SCHEDULED TASK CRUD
# ============================================================

def get_scheduled_tasks(
    db,
    user_id,
):

    return (
        db.query(ScheduledTask)
        .filter(
            ScheduledTask.user_id == user_id
        )
        .order_by(
            ScheduledTask.date,
            ScheduledTask.start_time
        )
        .all()
    )


def delete_scheduled_tasks(
    db,
    user_id,
):

    tasks = (
        db.query(ScheduledTask)
        .filter(
            ScheduledTask.user_id == user_id
        )
        .all()
    )

    for task in tasks:

        db.delete(task)

    db.commit()


# ============================================================
# USER-SPECIFIC DELETE ALL TASKS
# ============================================================

def delete_all_tasks(
    db,
    user_id,
):

    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == user_id
        )
        .all()
    )

    for task in tasks:

        db.delete(task)

    db.commit()


# ============================================================
# USER-SPECIFIC TASK STATISTICS
# ============================================================

def get_task_statistics(
    db,
    user_id,
):

    tasks = get_tasks(db, user_id)

    total = len(tasks)

    completed = len(
        [
            task
            for task in tasks
            if task.status == "Completed"
        ]
    )

    pending = len(
        [
            task
            for task in tasks
            if task.status == "Pending"
        ]
    )

    productivity = 0

    if total > 0:

        productivity = round(
            (completed / total) * 100
        )

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "productivity": productivity,
    }