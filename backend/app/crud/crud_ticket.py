from typing import Optional, List

from app.crud.base import CRUDBase
from app.models.ticket import Ticket
from app.models.city import City
from app.schemas.ticket import TicketCreate, TicketUpdate
from sqlalchemy.orm import Session


class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    def get_multiple_by_city(
            self, db: Session, *, city_ids: List[str]) -> Optional[Ticket]:
        return db.query(
            self.model).filter(
            Ticket.city_id.in_(city_ids)).all()


ticket = CRUDTicket(Ticket)
