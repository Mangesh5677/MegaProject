from modules.ai.scheduler import generate_schedule


def run_planner(db):
    """
    Main AI Planner entry point.
    Currently calls the scheduler.
    Later it will include:
    - Deadline optimization
    - Multi-day scheduling
    - AI recommendations
    """
    return generate_schedule(db)