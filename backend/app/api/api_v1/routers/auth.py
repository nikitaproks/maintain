from datetime import timedelta
from typing import Any

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if not user.role:
        role = "GUEST"
    else:
        role = user.role.name
    token_payload = {
        "id": str(user.id),
        "role": role,
        "email": str(user.email),
    }
    token, expire_date = security.create_token(
        token_payload, expires_delta=access_token_expires
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "exp": expire_date
    }


@router.post("/test-token", response_model=schemas.User)
def test_token(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/hash-password", response_model=str)
def hash_password(password: str = Body(..., embed=True),) -> Any:
    """
    Hash a password
    """
    return security.get_password_hash(password)
