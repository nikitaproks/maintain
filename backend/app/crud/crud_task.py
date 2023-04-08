from typing import Optional, List

from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def get_multiple_by_city(
            self, db: Session, *, city_ids: List[str]) -> Optional[Task]:
        return db.query(
            self.model).filter(
            Task.city_id.in_(city_ids)).all()


task = CRUDTask(Task)
