from fastapi import HTTPException, Path, APIRouter, Depends
from typing import Annotated
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from ..core.dependencies import get_current_owner
from ..core.security import hash_password
from ..database import get_db
from sqlmodel import Session, select
from ..models import (
    User,
    UserCreate,
    UserPublic,
)

users_router = APIRouter(dependencies=[Depends(get_current_owner)])


# USERS
@users_router.get("/", tags=["Usuarios"], response_model=Page[UserPublic])
def ver_usuarios(db: Session = Depends(get_db)):
    return paginate(db, select(User))


# USER
@users_router.get(
    "/{id}",
    tags=["Usuarios"],
    response_model=UserPublic,
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
@users_router.post("/", tags=["Usuarios"], response_model=UserPublic)
def agregar_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    nuevo_usuario = User(
        username=usuario.username,
        hashed_password=hash_password(usuario.password),
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


# REESCRIBIR USER
@users_router.put(
    "/{id}",
    tags=["Usuarios"],
    response_model=UserPublic,
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
    usuario_obtenido.hashed_password = hash_password(usuario.password)

    db.commit()
    db.refresh(usuario_obtenido)

    return usuario_obtenido


# BORRAR USER
@users_router.delete(
    "/{id}",
    tags=["Usuarios"],
    response_model=list[UserPublic],
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
