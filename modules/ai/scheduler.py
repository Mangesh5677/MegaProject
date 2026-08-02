from datetime import datetime, time, timedelta

from modules.database.models import Task, FixedSchedule


PRIORITY_ORDER = {
    "High": 0,
    "Medium": 1,
    "Low": 2,
}


def generate_schedule(db):

    today_name = datetime.now().strftime("%A")
    today_date = datetime.today().date()

    # Sort by priority, then deadline
    tasks = db.query(Task).filter(
        Task.status == "Pending"
    ).all()

    tasks.sort(
        key=lambda t: (
            PRIORITY_ORDER.get(t.priority, 3),
            t.due_date or today_date
        )
    )

    events = (
        db.query(FixedSchedule)
        .filter(FixedSchedule.day == today_name)
        .order_by(FixedSchedule.start_time)
        .all()
    )

    current = time(8, 0)
    day_end = time(22, 0)

    scheduled = []
    unscheduled = []

    for task in tasks:

        duration = timedelta(minutes=task.duration)

        while True:

            conflict = False

            # Check against today's classes
            for event in events:

                if current >= event.start_time and current < event.end_time:
                    current = event.end_time
                    conflict = True
                    break

            if conflict:
                continue

            start_dt = datetime.combine(today_date, current)
            end_dt = start_dt + duration

            # If task overlaps the next class, move it after that class
            overlap = False

            for event in events:

                event_start = datetime.combine(today_date, event.start_time)
                event_end = datetime.combine(today_date, event.end_time)

                if start_dt < event_end and end_dt > event_start:
                    current = event.end_time
                    overlap = True
                    break

            if overlap:
                continue

            # End of working day
            if end_dt.time() > day_end:
                unscheduled.append(task)
                break

            # Save schedule
            task.scheduled_date = today_date
            task.scheduled_start = start_dt.time()
            task.scheduled_end = end_dt.time()

            scheduled.append(task)

            current = end_dt.time()

            break

    db.commit()

    return scheduled, unscheduled