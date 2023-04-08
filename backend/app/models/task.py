import datetime
from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Task(Base):
    """
    Database Model for a task
    """

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    name = Column(String(255), default="Enter name")
    description = Column(String(100))
    status = Column(String(255), default="ToDo")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    assignee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True, default=None)
    assignee = relationship(
        "User",
        back_populates="tasks_assigned")

    city_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cities.id"),
        nullable=True, default=None)
    city = relationship(
        "City",
        back_populates="tasks")

    ticket_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tickets.id"),
        nullable=True, default=None)
    ticket = relationship(
        "Ticket",
        back_populates="tasks")
