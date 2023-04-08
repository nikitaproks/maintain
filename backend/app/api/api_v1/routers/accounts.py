from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from fastapi import APIRouter, Body, Depends, HTTPException, Security
from pydantic.types import UUID4
from sqlalchemy.orm import Session

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/{account_id}/",
            response_model=schemas.AccountFull,
            status_code=201,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
                Role.ACCOUNT_ADMIN["name"],
            ]))],
            )
def get_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: UUID4,
    current_user: models.User = Security(
        deps.get_current_active_user
    ),
) -> Any:
    """
    Get account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="account does not exist",
        )

    deps.check_account_ownership(current_user, account.owner_id)
    return account


@router.post("",
             response_model=schemas.Account,
             status_code=201,
             dependencies=[Depends(deps.RoleChecker([
                 Role.ADMIN["name"],
                 Role.SUPER_ADMIN["name"],
                 Role.ACCOUNT_ADMIN["name"],
             ]))],
             )
def create_account(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.AccountCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Create an account
    """
    account = crud.account.get_by_name(db, name=account_in.name)
    if account:
        raise HTTPException(
            status_code=409,
            detail="An account with this name already exists",)
    account_in.owner_id = current_user.id
    account = crud.account.create(db, obj_in=account_in)
    account.users.append(current_user)
    account = crud.account.change(db, db_obj=account)
    return account


@router.put("/{account_id}",
            response_model=schemas.Account,
            status_code=201,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
                Role.ACCOUNT_ADMIN["name"],
            ]))],
            )
def update_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: UUID4,
    account_in: schemas.AccountUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Update an account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="account does not exist",
        )

    deps.check_account_ownership(current_user, account.owner_id)

    account = crud.account.update(
        db, db_obj=account, obj_in=account_in)

    return account


@router.delete("/{account_id}",
               status_code=201,
               dependencies=[Depends(deps.RoleChecker([
                   Role.ADMIN["name"],
                   Role.SUPER_ADMIN["name"],
                   Role.ACCOUNT_ADMIN["name"],
               ]))],
               )
def delete_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: UUID4,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Update an account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="account does not exist",
        )

    deps.check_account_ownership(current_user, account.owner_id)

    crud.account.delete(
        db, id=account.id)

    return "Account was successfully deleted"

# Account user management


@router.post("/{account_id}/users",
             response_model=schemas.AccountFull,
             status_code=201,
             dependencies=[Depends(deps.RoleChecker([
                 Role.ADMIN["name"],
                 Role.SUPER_ADMIN["name"],
                 Role.ACCOUNT_ADMIN["name"],
             ]))],
             )
def add_user_to_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: UUID4,
    user_id: str = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a user to an account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="account does not exist",
        )
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="User does not exist",
        )

    deps.check_account_ownership(current_user, account.owner_id)

    account.users.append(user)
    account = crud.account.change(db, db_obj=account)
    return account


@router.post("/{account_id}/users/delete",
             response_model=schemas.AccountFull,
             status_code=201,
             dependencies=[Depends(deps.RoleChecker([
                 Role.ADMIN["name"],
                 Role.SUPER_ADMIN["name"],
                 Role.ACCOUNT_ADMIN["name"],
             ]))],
             )
def delete_user_from_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: UUID4,
    user_id: str = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a user to an account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="account does not exist",
        )
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="User does not exist",
        )

    if user not in account.users:
        raise HTTPException(
            status_code=404,
            detail=("User is not assigned to this account"),
        )

    deps.check_account_ownership(current_user, account.owner_id)

    account.users.remove(user)
    account = crud.account.change(db, db_obj=account)
    return account


# Account city management
@router.post("/{account_id}/cities",
             response_model=schemas.AccountFull,
             status_code=201,
             dependencies=[Depends(deps.RoleChecker([
                 Role.ADMIN["name"],
                 Role.SUPER_ADMIN["name"],
                 Role.ACCOUNT_ADMIN["name"],
             ]))],
             )
def add_city_to_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: UUID4,
    city_name: str = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a city to an account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="account does not exist",
        )
    city = crud.city.get_by_name(db, name=city_name)
    if not city:
        raise HTTPException(
            status_code=404, detail="city does not exist",
        )

    deps.check_account_ownership(current_user, account.owner_id)

    account.cities.append(city)
    account = crud.account.change(db, db_obj=account)
    return account


@router.post("/{account_id}/cities/delete",
             response_model=schemas.AccountFull,
             status_code=201,
             dependencies=[Depends(deps.RoleChecker([
                 Role.ADMIN["name"],
                 Role.SUPER_ADMIN["name"],
                 Role.ACCOUNT_ADMIN["name"],
             ]))],
             )
def delete_user_from_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: UUID4,
    city_name: str = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a city to an account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="account does not exist",
        )
    city = crud.city.get_by_name(db, name=city_name)
    if not city:
        raise HTTPException(
            status_code=404, detail="city does not exist",
        )

    if city not in account.cities:
        raise HTTPException(
            status_code=404,
            detail=("City is not assigned to this account"),
        )

    deps.check_account_ownership(current_user, account.owner_id)

    account.cities.remove(city)
    account = crud.account.change(db, db_obj=account)
    return account

# Admin account section


@router.get("", response_model=List[schemas.AccountFull])
def get_accounts(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all accounts.
    """
    accounts = crud.account.get_multi(db, skip=skip, limit=limit)
    return accounts
