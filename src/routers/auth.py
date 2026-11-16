
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ..database import get_db
from ..models import User
from ..core.security import verify_password, jwt_manager


auth_router = APIRouter()


@auth_router.post("/login", tags=["Autenticación"])
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    usuario = db.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not usuario or not verify_password(
        form_data.password,
        usuario.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = jwt_manager.create_access_token(
        data={"sub": usuario.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
