from fastapi import HTTPException, Path, APIRouter, Depends
from typing import Annotated
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from ..database import get_db
from sqlmodel import Session, select
from ..models import (
    User,
    UserCreate,
    UserRead,
)

users_router = APIRouter()


# USERS
@users_router.get("/", tags=["Usuarios"], response_model=Page[UserRead])
def ver_usuarios(db: Session = Depends(get_db)):
    return paginate(db, select(User))


# USER
@users_router.get(
    "/{id}",
    tags=["Usuarios"],
    response_model=UserRead,
    responses={
        404: {
            "description": "Usuario no encontrado",
            "content": {
                "application/json": {"example": {"detail": "Usuario no encontrado"}}
            },
        }
    },
)
def ver_usuario(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    usuario_obtenido = db.get(User, id)

    if not usuario_obtenido:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario_obtenido


# AGREGAR USER
@users_router.post("/", tags=["Usuarios"], response_model=UserRead)
def agregar_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    nuevo_usuario = User(
        username=usuario.username,
        hashed_password=usuario.password,
        is_owner=usuario.is_owner,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


# REESCRIBIR USER
@users_router.put(
    "/{id}",
    tags=["Usuarios"],
    response_model=UserRead,
    responses={
        404: {
            "description": "Usuario no encontrado",
            "content": {
                "application/json": {"example": {"detail": "Usuario no encontrado"}}
            },
        }
    },
)
def reescribir_usuario(
    id: Annotated[int, Path(gt=0)], usuario: UserCreate, db: Session = Depends(get_db)
):
    usuario_obtenido = db.get(User, id)

    if not usuario_obtenido:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario_obtenido.username = usuario.username
    usuario_obtenido.hashed_password = usuario.password
    usuario_obtenido.is_owner = usuario.is_owner

    db.commit()
    db.refresh(usuario_obtenido)

    return usuario_obtenido


# BORRAR USER
@users_router.delete(
    "/{id}",
    tags=["Usuarios"],
    response_model=list[UserRead],
    responses={
        404: {
            "description": "Usuario no encontrado",
            "content": {
                "application/json": {"example": {"detail": "Usuario no encontrado"}}
            },
        }
    },
)
def borrar_usuario(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    usuario_obtenido = db.get(User, id)

    if not usuario_obtenido:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario_obtenido)
    db.commit()

    return db.exec(select(User)).all()
