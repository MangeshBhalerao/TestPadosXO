from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from .database import Base


class Note(Base):
     __tablename__ = "notes"

     id = Column(Integer, primary_key=True, index=True)
     title = Column(String(100), nullable=False)
     content = Column(Text, nullable=False)
     created_at = Column(
          DateTime,
          default=lambda: datetime.now(timezone.utc),
          nullable=False
          )