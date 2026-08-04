from modules.database.database import Base, engine
import modules.database.models

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("✅ All database tables created successfully!")