from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel
from app.schemas import User


# Shared properties
class TaskBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


# Properties to receive via API on creation
class TaskCreate(TaskBase):
    city_id: Optional[UUID4]
    ticket_id: Optional[UUID4]


# Properties to receive via API on update
class TaskUpdate(TaskCreate):
    status: Optional[str]
    assignee_id: Optional[UUID4]


class Task(TaskUpdate):
    id: UUID4
    assignee: Optional[User]
    city: 'Optional[City]'
    # ticket: 'Optional[Ticket]'
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


from app.schemas.city import City  # noqa
from app.schemas.ticket import Ticket  # noqa
Task.update_forward_refs()
