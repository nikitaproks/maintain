from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from fastapi import APIRouter, Depends, HTTPException, Security
from pydantic.types import UUID4
from sqlalchemy.orm import Session

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users",
            response_model=List[schemas.UserFull],
            status_code=200,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
            ]))],
            )
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Admin retrieve all users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit,)
    return users


@router.get("/users/{user_id}",
            response_model=schemas.User,
            status_code=200,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
            ]))],
            )
def read_user_by_id(
    user_id: UUID4,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Admin get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    return user


@router.post("/users/create",
             response_model=schemas.User,
             status_code=200,
             dependencies=[Depends(deps.RoleChecker([
                 Role.ADMIN["name"],
                 Role.SUPER_ADMIN["name"],
             ]))],
             )
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate
) -> Any:
    """
    Admin create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/users/{user_id}",
            response_model=schemas.User,
            status_code=201,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
            ]))],
            )
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
    user_in: schemas.UserUpdate
) -> Any:
    """
    Admin update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/users/{user_id}",
               response_model=schemas.User,
               status_code=200,
               dependencies=[Depends(deps.RoleChecker([
                   Role.ADMIN["name"],
                   Role.SUPER_ADMIN["name"],
               ]))],
               )
def delete_user_by_id(
    user_id: UUID4,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Admin delete a specific user by id.
    """
    user = crud.user.delete(db, id=user_id)
    return user
