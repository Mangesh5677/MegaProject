from modules.database.database import Base, engine
import modules.database.models

Base.metadata.create_all(bind=engine)

print("✅ All database tables created successfully!")