from app import crud, schemas
from app.constants.role import Role
from app.core.config import settings
from app.db.base_class import Base
from app.db.session import engine
from sqlalchemy.orm import Session


def create_database():
    return Base.metadata.create_all(bind=engine)


def init_db(db: Session) -> None:
    create_database()
    # Create Super Admin Account
    account = crud.account.get_by_name(
        db, name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME
    )
    if not account:
        account_in = schemas.AccountCreate(
            name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME,
            description="superadmin account",
        )
        crud.account.create(db, obj_in=account_in)

    # Create Role If They Don't Exist
    guest_role = crud.role.get_by_name(db, name=Role.GUEST["name"])
    if not guest_role:
        guest_role_in = schemas.RoleCreate(
            name=Role.GUEST["name"],
            description=Role.GUEST["description"])
        crud.role.create(db, obj_in=guest_role_in)

    account_member_role = crud.role.get_by_name(
        db, name=Role.ACCOUNT_MEMEBER["name"])
    if not account_member_role:
        account_member_role_in = schemas.RoleCreate(
            name=Role.ACCOUNT_MEMEBER["name"],
            description=Role.ACCOUNT_MEMEBER["description"])
        crud.role.create(db, obj_in=account_member_role_in)

    account_admin_role = crud.role.get_by_name(
        db, name=Role.ACCOUNT_ADMIN["name"]
    )
    if not account_admin_role:
        account_admin_role_in = schemas.RoleCreate(
            name=Role.ACCOUNT_ADMIN["name"],
            description=Role.ACCOUNT_ADMIN["description"],
        )
        crud.role.create(db, obj_in=account_admin_role_in)

    fleet_manager_role = crud.role.get_by_name(
        db, name=Role.FLEET_MANAGER["name"]
    )
    if not fleet_manager_role:
        fleet_manager_role_in = schemas.RoleCreate(
            name=Role.FLEET_MANAGER["name"],
            description=Role.FLEET_MANAGER["description"],
        )
        crud.role.create(db, obj_in=fleet_manager_role_in)

    account_manager_role = crud.role.get_by_name(
        db, name=Role.ACCOUNT_ADMIN["name"]
    )
    if not account_manager_role:
        account_manager_role_in = schemas.RoleCreate(
            name=Role.ACCOUNT_ADMIN["name"],
            description=Role.ACCOUNT_ADMIN["description"],
        )
        crud.role.create(db, obj_in=account_manager_role_in)

    admin_role = crud.role.get_by_name(db, name=Role.ADMIN["name"])
    if not admin_role:
        admin_role_in = schemas.RoleCreate(
            name=Role.ADMIN["name"],
            description=Role.ADMIN["description"])
        crud.role.create(db, obj_in=admin_role_in)

    super_admin_role = crud.role.get_by_name(
        db, name=Role.SUPER_ADMIN["name"])
    if not super_admin_role:
        super_admin_role_in = schemas.RoleCreate(
            name=Role.SUPER_ADMIN["name"],
            description=Role.SUPER_ADMIN["description"],
        )
        crud.role.create(db, obj_in=super_admin_role_in)
    # Create 1st Superuser
    user = crud.user.get_by_email(
        db, email=settings.FIRST_SUPER_ADMIN_EMAIL)
    if not user:
        account = crud.account.get_by_name(
            db, name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME
        )
        super_admin_role = crud.role.get_by_name(
            db, name=Role.SUPER_ADMIN["name"]
        )

        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPER_ADMIN_EMAIL,
            password=settings.FIRST_SUPER_ADMIN_PASSWORD,
            full_name=settings.FIRST_SUPER_ADMIN_EMAIL,
            role_id=super_admin_role.id
        )
        user = crud.user.create(db, obj_in=user_in)
