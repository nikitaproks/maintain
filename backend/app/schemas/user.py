from datetime import datetime
from typing import Optional, List
from app.schemas.role import Role
from pydantic import UUID4, BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    phone_number: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    role_id: UUID4


# Properties to receive via API on update
class UserUpdate(UserBase):
    role_id: Optional[UUID4]


class User(UserBase):
    id: UUID4
    role: Role
    # tickets_reported: List[Ticket]

    class Config:
        orm_mode = True


class UserFull(User):
    accounts: "List[Account]"
    created_at: datetime
    updated_at: datetime


class UserInDB(UserFull):
    hashed_password: str


from app.schemas.account import Account  # noqa
UserFull.update_forward_refs()
