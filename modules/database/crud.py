from .models import FixedSchedule, Task


# ==========================================
# Fixed Schedule CRUD
# ==========================================

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
    schedule_id
):
    event = (
        db.query(FixedSchedule)
        .filter(
            FixedSchedule.id == schedule_id,
            FixedSchedule.user_id == user_id
        )
        .first()
    )

    if event:
        db.delete(event)
        db.commit()

    return event


# ==========================================
# Task CRUD
# ==========================================

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

        # Reminder flags
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
            Task.status == "Pending"
        )
        .order_by(
            Task.due_date,
            Task.due_time
        )
        .all()
    )


def delete_task(
    db,
    user_id,
    task_id
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id
        )
        .first()
    )

    if task:
        db.delete(task)
        db.commit()

        return task

    return None


def complete_task(
    db,
    user_id,
    task_id
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id
        )
        .first()
    )

    if task:
        task.status = "Completed"

        db.commit()
        db.refresh(task)

        return task

    return None


# ==========================================
# Reminder CRUD
# ==========================================

def mark_24h_reminder_sent(
    db,
    user_id,
    task_id
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id
        )
        .first()
    )

    if task:
        task.reminder_24h_sent = True
        db.commit()
        db.refresh(task)

        return task

    return None


def mark_2h_reminder_sent(
    db,
    user_id,
    task_id
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id
        )
        .first()
    )

    if task:
        task.reminder_2h_sent = True
        db.commit()
        db.refresh(task)

        return task

    return None


def mark_30m_reminder_sent(
    db,
    user_id,
    task_id
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id
        )
        .first()
    )

    if task:
        task.reminder_30m_sent = True
        db.commit()
        db.refresh(task)

        return task

    return None