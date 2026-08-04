from .models import FixedSchedule, Task


# ==========================
# Fixed Schedule CRUD
# ==========================

def add_fixed_schedule(db, day, title, category, start_time, end_time):
    event = FixedSchedule(
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


def get_fixed_schedules(db):
    return db.query(FixedSchedule).all()


def delete_fixed_schedule(db, schedule_id):
    event = (
        db.query(FixedSchedule)
        .filter(FixedSchedule.id == schedule_id)
        .first()
    )

    if event:
        db.delete(event)
        db.commit()


# ==========================
# Task CRUD
# ==========================

def add_task(
    db,
    title,
    description,
    priority,
    due_date,
    due_time,
    duration,
    email,
):
    task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        due_time=due_time,
        duration=duration,
        email=email,
        reminder_24h_sent=False,
        reminder_2h_sent=False,
        reminder_30m_sent=False,
        status="Pending",
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db):
    return db.query(Task).all()


def get_pending_tasks(db):
    return (
        db.query(Task)
        .filter(Task.status == "Pending")
        .all()
    )


def delete_task(db, task_id):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task:
        db.delete(task)
        db.commit()


def complete_task(db, task_id):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task:
        task.status = "Completed"
        db.commit()