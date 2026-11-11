from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_db
from ..models import User, UserCreate, UserRead

router = APIRouter(prefix="/users")


@router.post(
    "/", response_model=UserRead, status_code=status.HTTP_201_CREATED, tags=["Usuarios"]
)
def crear_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    db_user = User.from_orm(usuario)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=list[UserRead], tags=["Usuarios"])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios = db.exec(select(User).offset(skip).limit(limit)).all()
    return usuarios
    usuarios = db.exec(select(User).offset(skip).limit(limit)).all()
    return usuarios


@router.get("/{user_id}", response_model=UserRead, tags=["Usuarios"])
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.get(User, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{user_id}", response_model=UserRead, tags=["Usuarios"])
def actualizar_usuario(
    user_id: int, usuario_update: UserCreate, db: Session = Depends(get_db)
):
    usuario = db.get(User, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    datos = usuario_update.dict()
    for key, value in datos.items():
        setattr(usuario, key, value)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def borrar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.get(User, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return None
