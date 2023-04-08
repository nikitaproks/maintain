from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from fastapi import APIRouter, Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("",
            response_model=List[schemas.Task],
            status_code=200,
            dependencies=[Depends(deps.RoleChecker([
                Role.SUPER_ADMIN["name"],
                Role.ADMIN["name"],
                Role.FLEET_MANAGER["name"],
                Role.ACCOUNT_ADMIN["name"],
            ]))],
            )
def get_tasks(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    city: str | None = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get tasks.
    """

    if city:
        city = crud.city.get_by_name(db, name=city)
        if not city:
            raise HTTPException(
                status_code=404, detail="city does not exist",
            )
        deps.check_user_city_scope(current_user, city)
        return crud.task.get_multiple_by_city(
            db, city_ids=[city.id])

    admin_roles = [
        Role.SUPER_ADMIN["name"],
        Role.ADMIN["name"],
        Role.FLEET_MANAGER["name"]]
    if current_user.role.name in admin_roles:
        return crud.task.get_multi(db, skip=skip, limit=limit)

    user_cities_ids = deps.get_user_city_scope(current_user)
    task = crud.task.get_multiple_by_city(
        db, city_ids=user_cities_ids)
    return task


@router.get("/{task_id}",
            response_model=schemas.Task,
            status_code=200,
            dependencies=[Depends(deps.RoleChecker([
                Role.SUPER_ADMIN["name"],
                Role.ADMIN["name"],
                Role.FLEET_MANAGER["name"],
                Role.ACCOUNT_ADMIN["name"],
                Role.ACCOUNT_MEMEBER["name"],
            ]))],
            )
def get_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: UUID4,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get task
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=404, detail="task does not exist",
        )

    deps.check_user_city_scope(current_user, task.city)

    return task


@router.post("",
             response_model=schemas.Task,
             status_code=201,
             dependencies=[Depends(deps.RoleChecker([
                 Role.SUPER_ADMIN["name"],
                 Role.ADMIN["name"],
                 Role.FLEET_MANAGER["name"],
                 Role.ACCOUNT_ADMIN["name"],
                 Role.ACCOUNT_MEMEBER["name"],
             ]))],
             )
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a task
    """

    if task_in.city_id:
        city = crud.city.get(db, id=task_in.city_id)
        if not city:
            raise HTTPException(
                status_code=404, detail="city does not exist",
            )
        deps.check_user_city_scope(current_user, city)

    if task_in.ticket_id:
        ticket = crud.ticket.get(db, id=task_in.ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=404, detail="ticket does not exist",
            )
        deps.check_user_city_scope(current_user, ticket.city)
    task = crud.task.create(db, obj_in=task_in)
    return task


@router.put("/{task_id}",
            response_model=schemas.Task,
            status_code=201,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
                Role.FLEET_MANAGER["name"],
                Role.ACCOUNT_ADMIN["name"],
                Role.ACCOUNT_MEMEBER["name"],
            ]))],
            )
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: UUID4,
    task_in: schemas.TaskUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Update a task.
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=404, detail="ticket does not exist",
        )

    if task_in.city_id:
        city = crud.city.get(db, id=task_in.city_id)
        if not city:
            raise HTTPException(
                status_code=404, detail="city does not exist",
            )
        deps.check_user_city_scope(current_user, city)

    if task_in.ticket_id:
        ticket = crud.ticket.get(db, id=task_in.ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=404, detail="ticket does not exist",
            )
        deps.check_user_city_scope(current_user, ticket.city)

    if task_in.assignee_id:
        user = crud.user.get(db, id=task_in.assignee_id)
        if not user:
            raise HTTPException(
                status_code=404, detail="user does not exist",
            )

    deps.check_user_city_scope(current_user, task.city)
    task = crud.task.update(
        db, db_obj=task, obj_in=task_in)

    return task


@router.delete("/{task_id}",
               status_code=200,
               dependencies=[Depends(deps.RoleChecker([
                   Role.ADMIN["name"],
                   Role.SUPER_ADMIN["name"],
                   Role.FLEET_MANAGER["name"],
                   Role.ACCOUNT_ADMIN["name"],
                   Role.ACCOUNT_MEMEBER["name"],
               ]))],
               )
def delete_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: UUID4,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Delete a task.
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=404, detail="task does not exist",
        )

    deps.check_user_city_scope(current_user, task.city)
    crud.task.delete(
        db, id=task_id)
    return {"result": "success"}
