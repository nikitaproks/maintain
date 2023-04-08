from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel
from app.schemas import User


# Shared properties
class TicketBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    city_id: Optional[UUID4]


# Properties to receive via API on creation
class TicketCreate(TicketBase):
    reporter_id: UUID4


# Properties to receive via API on update
class TicketUpdate(TicketBase):
    status: Optional[str]
    assignee_id: Optional[UUID4]


class Ticket(TicketBase):
    id: UUID4
    status: str
    reporter: User
    assignee: Optional[User]
    city: 'Optional[City]'
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


from app.schemas.city import City  # noqa
Ticket.update_forward_refs()
