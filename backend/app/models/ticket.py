import datetime
from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Ticket(Base):
    """
    Database Model for a ticket
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

    reporter_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    reporter = relationship(
        "User", foreign_keys=[reporter_id],
        back_populates="tickets_reported")

    assignee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True, default=None)
    assignee = relationship(
        "User", foreign_keys=[assignee_id],
        back_populates="tickets_assigned")

    city_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cities.id"),
        nullable=True, default=None)
    city = relationship(
        "City",
        back_populates="tickets")

    tasks = relationship(
        "Task",
        back_populates="ticket")
