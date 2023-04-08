from datetime import datetime
from typing import Optional, Any, List, TYPE_CHECKING
from pydantic import UUID4, BaseModel


class AccountBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class AccountCreate(AccountBase):
    owner_id: Optional[Any]


# Properties to receive via API on update
class AccountUpdate(AccountCreate):
    pass


class Account(AccountUpdate):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    cities: "List[City]"

    class Config:
        orm_mode = True


class AccountFull(Account):
    users: "List[User]"


class AccountInDB(AccountFull):
    pass


from app.schemas.user import User  # noqa
from app.schemas.city import City  # noqa
Account.update_forward_refs()
AccountFull.update_forward_refs()
