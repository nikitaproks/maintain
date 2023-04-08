from datetime import datetime
from typing import Optional, List
from pydantic import UUID4, BaseModel


class CityBase(BaseModel):
    name: Optional[str]


# Properties to receive via API on creation
class CityCreate(CityBase):
    pass


# Properties to receive via API on update
class CityUpdate(CityCreate):
    pass


class City(CityUpdate):
    id: UUID4
    created_at: datetime

    class Config:
        orm_mode = True


class CityFull(City):
    accounts: "List[Account]"


class CityInDB(CityFull):
    pass


from app.schemas.account import Account  # noqa
CityFull.update_forward_refs()
