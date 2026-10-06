from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker
import os

os.makedirs("data/db", exist_ok=True)

DATABASE_URL = "sqlite:///data/db/productivity.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def ensure_database_schema():
    inspector = inspect(engine)
    if "tasks" not in inspector.get_table_names():
        Base.metadata.create_all(bind=engine)
        return

    existing_columns = {col["name"] for col in inspector.get_columns("tasks")}
    with engine.begin() as conn:
        if "task_type" not in existing_columns:
            conn.execute(
                text("ALTER TABLE tasks ADD COLUMN task_type VARCHAR DEFAULT 'Once'")
            )
        if "assigned_by_id" not in existing_columns:
            conn.execute(
                text("ALTER TABLE tasks ADD COLUMN assigned_by_id INTEGER")
            )


ensure_database_schema()