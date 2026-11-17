from fastapi import HTTPException, Path, APIRouter, Depends, status
from typing import Annotated
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from ..core.dependencies import get_current_owner, get_optional_user
from ..core.security import hash_password
from ..database import get_db
from sqlmodel import Session, select
from ..models import (
    User,
    UserCreate,
    UserPublic,
)

users_router = APIRouter()


# USERS
@users_router.get(
    "/",
    tags=["Usuarios"],
    response_model=Page[UserPublic],
    dependencies=[Depends(get_current_owner)],
)
def ver_usuarios(db: Session = Depends(get_db)):
    return paginate(db, select(User))


# USER
@users_router.get(
    "/{id}",
    tags=["Usuarios"],
    response_model=UserPublic,
    dependencies=[Depends(get_current_owner)],
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
def agregar_usuario(
    usuario: UserCreate,
    db: Session = Depends(get_db),
    usuario_actual: User | None = Depends(get_optional_user),
):
    usuario_existente = db.exec(select(User.id).limit(1)).first()

    if usuario_existente is None:
        primer_usuario = True
    else:
        if usuario_actual is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Se requiere autenticación",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not usuario_actual.is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Se requieren permisos de propietario",
            )

        primer_usuario = False

    nuevo_usuario = User(
        username=usuario.username,
        hashed_password=hash_password(usuario.password),
        is_owner=primer_usuario,
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
    dependencies=[Depends(get_current_owner)],
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
    dependencies=[Depends(get_current_owner)],
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

    if usuario_obtenido.is_owner:
        propietarios = db.exec(select(User).where(User.is_owner == True)).all()

        if len(propietarios) <= 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar al último propietario",
            )

    db.delete(usuario_obtenido)
    db.commit()

    return db.exec(select(User)).all()
