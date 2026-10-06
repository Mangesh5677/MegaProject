from modules.database.database import engine, Base

# Import ALL models so SQLAlchemy knows about their tables
from modules.database.models import User

# Import activity model
from modules.database.activity import UserActivity


print("Updating database...")

Base.metadata.create_all(bind=engine)

print("User activity table created successfully.")