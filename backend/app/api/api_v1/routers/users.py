from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.core.config import settings
from fastapi import APIRouter, Body, Depends, HTTPException, Security
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from pydantic.types import UUID4
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserFull)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return schemas.UserFull.from_orm(current_user)


@router.post("/register", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(...),
    phone_number: str = Body(None),
) -> Any:
    """
    Create new user.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this email already exists in the system",
        )
    role = crud.role.get_by_name(db, name="GUEST")
    user_in = schemas.UserCreate(
        password=password,
        email=email,
        full_name=full_name,
        phone_number=phone_number,
        role_id=role.id
    )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    full_name: str = Body(None),
    phone_number: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if phone_number is not None:
        user_in.phone_number = phone_number
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


# USER admin section


@router.get("/admin/{user_id}",
            response_model=schemas.User,
            status_code=200,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
            ]))],
            )
def admin_get_user(
    user_id: UUID4,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Admin get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    return user


@router.post("/admin/create",
             response_model=schemas.User,
             status_code=200,
             dependencies=[Depends(deps.RoleChecker([
                 Role.ADMIN["name"],
                 Role.SUPER_ADMIN["name"],
             ]))],
             )
def admin_create_user(
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


@router.put("/admin/{user_id}",
            response_model=schemas.User,
            status_code=201,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
            ]))],
            )
def admin_update_user(
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


@router.delete("/admin/{user_id}",
               response_model=schemas.User,
               status_code=200,
               dependencies=[Depends(deps.RoleChecker([
                   Role.ADMIN["name"],
                   Role.SUPER_ADMIN["name"],
               ]))],
               )
def admin_delete_user(
    user_id: UUID4,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Admin delete a specific user by id.
    """
    user = crud.user.delete(db, id=user_id)
    return user


@router.get("/admin/",
            response_model=List[schemas.UserFull],
            status_code=200,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
            ]))],
            )
def admin_get_all_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Admin retrieve all users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit,)
    return users
