from datetime import time


def find_free_slots(events):

    day_start = time(8, 0)
    day_end = time(22, 0)

    free_slots = []

    current = day_start

    for event in events:

        # Free time before this event
        if current < event.start_time:
            free_slots.append((current, event.start_time))

        # Move current pointer
        if event.end_time > current:
            current = event.end_time

    # Remaining time after last event
    if current < day_end:
        free_slots.append((current, day_end))

    return free_slots