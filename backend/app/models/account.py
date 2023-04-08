import datetime
from uuid import uuid4

from app.models.dependencies import association_table_user_account, association_table_account_city
from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Account(Base):
    """
    Database model for an account
    """

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    name = Column(String(255), index=True, nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean(), default=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    owner = relationship("User", back_populates="owned_accounts")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    users = relationship(
        "User", secondary=association_table_user_account,
        back_populates="accounts")

    cities = relationship(
        "City", secondary=association_table_account_city,
        back_populates="accounts")
