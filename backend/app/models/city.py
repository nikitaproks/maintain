import datetime
from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.dependencies import association_table_account_city


class City(Base):
    """
    Database Model for a city
    """

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String(255), unique=True)
    accounts = relationship(
        "Account", secondary=association_table_account_city,
        back_populates="cities")

    tickets = relationship(
        "Ticket",
        back_populates="city")

    tasks = relationship(
        "Task",
        back_populates="city")
