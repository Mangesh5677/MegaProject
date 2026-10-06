from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from modules.database.database import Base


class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    activity_type = Column(
        String,
        nullable=False
    )

    activity_details = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )