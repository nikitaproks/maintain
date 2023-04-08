from typing import Optional

from app.crud.base import CRUDBase
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate
from sqlalchemy.orm import Session


class CRUDCity(CRUDBase[City, CityCreate, CityUpdate]):
    def get_by_name(
            self, db: Session, *, name: str) -> Optional[City]:
        return db.query(
            self.model).filter(
            City.name == name).first()


city = CRUDCity(City)
