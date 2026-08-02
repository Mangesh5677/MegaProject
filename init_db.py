from modules.database.database import engine
from modules.database.models import Base

Base.metadata.create_all(bind=engine)

print("✅ Database created successfully!")