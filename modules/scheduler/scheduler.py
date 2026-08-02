from datetime import datetime, timedelta

from modules.database.models import Task, FixedSchedule
from modules.ai.free_slots import find_free_slots


PRIORITY_ORDER = {
    "High": 0,
    "Medium": 1,
    "Low": 2,
}


def generate_schedule(db):

    today = datetime.today().date()
    weekday = today.strftime("%A")

    # Get pending tasks
    tasks = db.query(Task).filter(
        Task.status == "Pending"
    ).all()

    # Sort by priority and deadline
    tasks.sort(
        key=lambda t: (
            PRIORITY_ORDER.get(t.priority, 3),
            t.due_date or today
        )
    )

    # Get today's fixed timetable
    events = (
        db.query(FixedSchedule)
        .filter(FixedSchedule.day == weekday)
        .order_by(FixedSchedule.start_time)
        .all()
    )

    # Find free slots
    free_slots = find_free_slots(events)

    scheduled = []
    unscheduled = []

    for task in tasks:

        placed = False
        duration = timedelta(minutes=task.duration)

        for i, (slot_start, slot_end) in enumerate(free_slots):

            start_dt = datetime.combine(today, slot_start)
            end_dt = datetime.combine(today, slot_end)

            # Check whether the task fits
            if end_dt - start_dt >= duration:

                finish = start_dt + duration

                task.scheduled_date = today
                task.scheduled_start = start_dt.time()
                task.scheduled_end = finish.time()

                # Update remaining free slot
                free_slots[i] = (
                    finish.time(),
                    slot_end
                )

                scheduled.append(task)
                placed = True
                break

        if not placed:
            unscheduled.append(task)

    db.commit()

    return scheduled, unscheduled