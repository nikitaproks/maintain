import logging
import jwt
from typing import Any, Dict, List, Optional, Union, Generator
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.constants.role import Role
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer  # , SecurityScopes
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class OAuth2PasswordBearerCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


reusable_oauth2 = OAuth2PasswordBearerCookie(
    tokenUrl=f"{settings.API_V1_STR}/auth/access-token",
)

""" scopes={Role.GUEST["name"]: Role.GUEST["description"],
            Role.ACCOUNT_ADMIN["name"]: Role.ACCOUNT_ADMIN
            ["description"],
            Role.ACCOUNT_MANAGER["name"]: Role.ACCOUNT_MANAGER
            ["description"],
            Role.ADMIN["name"]: Role.ADMIN["description"],
            Role.SUPER_ADMIN["name"]: Role.SUPER_ADMIN
            ["description"], } """

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> models.User:
    # if security_scopes.scopes:
    #     authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    # else:
    #     pass
    authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY,
            algorithms=[security.ALGORITHM])
        if payload.get("id") is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(**payload)
    except (jwt.ExpiredSignatureError, ValidationError):
        logger.error("Error Decoding Token", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    except jwt.DecodeError:
        logger.error("Error Decoding Token", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Corrupted token",
        )
    user = crud.user.get(db, id=token_data.id)

    """if not user:
        raise credentials_exception
    if roles and not token_data.role:
        raise HTTPException(
            status_code=401,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    if (
        roles
        and token_data.role not in roles
    ):
        raise HTTPException(
            status_code=401,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )"""
    return user


def get_current_active_user(
        current_user: models.User = Security(
            get_current_user),) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def check_account_ownership(current_user, account_owner_id):
    # If user is an account admin, check ensure they update their own account.
    admin_roles = [
        Role.ADMIN["name"],
        Role.SUPER_ADMIN["name"],
        Role.FLEET_MANAGER["name"]]
    if current_user.role.name not in admin_roles and current_user.id != account_owner_id:
        raise HTTPException(
            status_code=401,
            detail=(
                "This user does not have the permissions to "
                "manipulate this account"
            ),
        )


def get_user_city_scope(current_user):
    user_cities_ids = []
    for account in current_user.accounts:
        for account_city in account.cities:
            user_cities_ids.append(account_city.id)
    return user_cities_ids


def check_user_city_scope(current_user, city):
    user_cities = []
    admin_roles = [
        Role.SUPER_ADMIN["name"],
        Role.ADMIN["name"],
        Role.FLEET_MANAGER["name"]]
    if current_user.role.name not in admin_roles:
        user_cities_ids = get_user_city_scope(current_user)
        if city.id not in user_cities_ids:
            raise HTTPException(
                status_code=404,
                detail="This data is out of your scope",)


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: schemas.User = Depends(
            get_current_active_user)):
        if user.role.name not in self.allowed_roles:
            logger.debug(
                f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(
                status_code=403, detail="Operation not permitted")
