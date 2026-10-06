from sqlalchemy import inspect, text
from modules.database.database import engine

inspector = inspect(engine)

columns = [
    column["name"]
    for column in inspector.get_columns("users")
]

if "role" not in columns:
    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE users "
                "ADD COLUMN role VARCHAR NOT NULL DEFAULT 'user'"
            )
        )
    print("Role column added successfully.")
else:
    print("Role column already exists.")