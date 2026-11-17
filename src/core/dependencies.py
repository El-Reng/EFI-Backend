from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from ..database import get_db
from ..models import User
from .security import jwt_manager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False,
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    payload = jwt_manager.verify_token(token)

    username = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = db.exec(select(User).where(User.username == username)).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario


def get_current_owner(
    usuario: Annotated[User, Depends(get_current_user)],
) -> User:
    if not usuario.is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de propietario",
        )

    return usuario


def get_optional_user(
    token: Annotated[str | None, Depends(oauth2_scheme_optional)],
    db: Annotated[Session, Depends(get_db)],
) -> User | None:
    if token is None:
        return None

    payload = jwt_manager.verify_token(token)

    username = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = db.exec(select(User).where(User.username == username)).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario
