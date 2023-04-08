from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from fastapi import APIRouter, Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("",
            response_model=List[schemas.Ticket],
            status_code=200,
            dependencies=[Depends(deps.RoleChecker([
                Role.SUPER_ADMIN["name"],
                Role.ADMIN["name"],
                Role.FLEET_MANAGER["name"],
                Role.ACCOUNT_ADMIN["name"],
            ]))],
            )
def get_tickets(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    city: str | None = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get tickets.
    """

    if city:
        city = crud.city.get_by_name(db, name=city)
        if not city:
            raise HTTPException(
                status_code=404, detail="city does not exist",
            )

    admin_roles = [
        Role.SUPER_ADMIN["name"],
        Role.ADMIN["name"],
        Role.FLEET_MANAGER["name"]]
    if current_user.role.name not in admin_roles:
        user_cities = []
        for account in current_user.accounts:
            for account_city in account.cities:
                user_cities.append(account_city.id)

        if city:
            if city.id not in user_cities:
                raise HTTPException(
                    status_code=404,
                    detail="You do not have permission to access this data",)
            else:
                user_cities = [city.id]
        tickets = crud.ticket.get_multiple_by_city(
            db, city_ids=user_cities)
        print(tickets)

    else:
        tickets = crud.ticket.get_multi(db, skip=skip, limit=limit)
    return tickets


@router.get("/{ticket_id}",
            response_model=schemas.Ticket,
            status_code=200,
            dependencies=[Depends(deps.RoleChecker([
                Role.SUPER_ADMIN["name"],
                Role.ADMIN["name"],
                Role.FLEET_MANAGER["name"],
                Role.ACCOUNT_ADMIN["name"],
            ]))],
            )
def get_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_id: UUID4,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get ticket
    """
    ticket = crud.ticket.get(db, id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=404, detail="ticket does not exist",
        )

    admin_roles = [
        Role.SUPER_ADMIN["name"],
        Role.ADMIN["name"],
        Role.FLEET_MANAGER["name"]]
    if current_user.role.name not in admin_roles:
        user_cities = []
        for account in current_user.accounts:
            for account_city in account.cities:
                user_cities.append(account_city)

        if ticket.city not in user_cities:
            raise HTTPException(
                status_code=404,
                detail="This ticket is out of your scope",)

    return ticket


@router.post("",
             response_model=schemas.Ticket,
             status_code=201,
             dependencies=[Depends(deps.RoleChecker([
                 Role.SUPER_ADMIN["name"],
                 Role.ADMIN["name"],
                 Role.FLEET_MANAGER["name"],
                 Role.ACCOUNT_ADMIN["name"],
             ]))],
             )
def create_ticket(
    *,
    db: Session = Depends(deps.get_db),
    data: schemas.TicketBase,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a ticket
    """

    city = crud.city.get(db, id=data.city_id)
    if not city:
        raise HTTPException(
            status_code=404, detail="city does not exist",
        )

    data = jsonable_encoder(data)
    data["reporter_id"] = current_user.id
    data = schemas.TicketCreate(**data)
    ticket = crud.ticket.create(db, obj_in=data)
    return ticket


@router.put("/{ticket_id}",
            response_model=schemas.Ticket,
            status_code=201,
            dependencies=[Depends(deps.RoleChecker([
                Role.ADMIN["name"],
                Role.SUPER_ADMIN["name"],
                Role.FLEET_MANAGER["name"],
                Role.ACCOUNT_ADMIN["name"],
            ]))],
            )
def update_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_id: UUID4,
    ticket_in: schemas.TicketUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Update a ticket.
    """
    ticket = crud.ticket.get(db, id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=404, detail="ticket does not exist",
        )

    ticket = crud.ticket.update(
        db, db_obj=ticket, obj_in=ticket_in)

    return ticket


@router.delete("/{ticket_id}",
               status_code=200,
               dependencies=[Depends(deps.RoleChecker([
                   Role.ADMIN["name"],
                   Role.SUPER_ADMIN["name"],
                   Role.FLEET_MANAGER["name"],
                   Role.ACCOUNT_ADMIN["name"],
               ]))],
               )
def delete_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_id: UUID4,
    current_user: models.User = Security(
        deps.get_current_active_user,
    ),
) -> Any:
    """
    Delete a ticket.
    """
    ticket = crud.ticket.get(db, id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=404, detail="ticket does not exist",
        )

    crud.ticket.delete(
        db, id=ticket_id)

    return {"result": "the ticket was deleted"}
