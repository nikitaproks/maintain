from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Table
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

association_table_user_account = Table(
    'user_account_association', Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True,
           index=True, default=uuid4),
    Column('user_id', ForeignKey('users.id'),
           primary_key=True),
    Column(
        'account_id', ForeignKey('accounts.id'),
        primary_key=True))

association_table_account_city = Table(
    'account_city_association', Base.metadata,
    Column('city_id', ForeignKey('cities.id'),
           primary_key=True),
    Column(
        'account_id', ForeignKey('accounts.id'),
        primary_key=True))
