from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from fastapi import APIRouter, Body, Depends, HTTPException, Security
from pydantic.types import UUID4
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/{city_name}/",
            response_model=schemas.CityFull,
            status_code=200
            )
def get_city(
    *,
    db: Session = Depends(deps.get_db),
    city_name: str,
    current_user: models.User = Security(
        deps.get_current_active_user
    ),
) -> Any:
    """
    Get city.
    """
    city = crud.city.get_by_name(db, name=city_name)
    if not city:
        raise HTTPException(
            status_code=404, detail="city does not exist",
        )
    print(current_user.accounts[0].cities)

    return city


@router.post("",
             response_model=schemas.City,
             status_code=201,
             dependencies=[Depends(deps.RoleChecker([
                 Role.ADMIN["name"],
                 Role.SUPER_ADMIN["name"],
                 Role.ACCOUNT_ADMIN["name"],
             ]))],
             )
def create_city(
    *,
    db: Session = Depends(deps.get_db),
    city_in: schemas.CityCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Create a city
    """
    city = crud.city.get_by_name(db, name=city_in.name)
    if city:
        raise HTTPException(
            status_code=409,
            detail="A city with this name already exists",)
    city = crud.city.create(db, obj_in=city_in)
    return city


@router.put("/{account_id}",
            response_model=schemas.City,
            status_code=201,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
                Role.ACCOUNT_ADMIN["name"],
            ]))],
            )
def update_city(
    *,
    db: Session = Depends(deps.get_db),
    city_id: UUID4,
    city_in: schemas.CityUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Update an city.
    """
    city = crud.city.get(db, id=city_id)
    if not city:
        raise HTTPException(
            status_code=404, detail="city does not exist",
        )

    city = crud.city.update(
        db, db_obj=city, obj_in=city_in)

    return city


@router.delete("/{city_id}",
               status_code=201,
               dependencies=[Depends(deps.RoleChecker([
                   Role.ADMIN["name"],
                   Role.SUPER_ADMIN["name"]
               ]))],
               )
def delete_city(
    *,
    db: Session = Depends(deps.get_db),
    city_id: UUID4,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Update an city.
    """
    city = crud.city.get(db, id=city_id)
    if not city:
        raise HTTPException(
            status_code=404, detail="city does not exist",
        )

    crud.city.delete(
        db, id=city.id)

    return {"result": "City was successfully deleted"}


# Admin account section
@router.get("", response_model=List[schemas.City])
def get_cities(
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
    Retrieve all cities.
    """
    cities = crud.city.get_multi(db, skip=skip, limit=limit)
    return cities
