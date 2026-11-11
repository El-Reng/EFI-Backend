from fastapi import HTTPException, Path, APIRouter, Depends
from typing import Annotated
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from ..database import get_db
from sqlmodel import Session, select
from ..models import (
    Category,
    CategoryCreate,
    CategoryRead,
)

categories_router = APIRouter()


# CATEGORIES
@categories_router.get("/", tags=["Categorías"], response_model=Page[CategoryRead])
def ver_categorias(db: Session = Depends(get_db)):
    return paginate(db, select(Category))


# CATEGORY
@categories_router.get(
    "/{id}",
    tags=["Categorías"],
    response_model=CategoryRead,
    responses={
        404: {
            "description": "Categoría no encontrada",
            "content": {
                "application/json": {"example": {"detail": "Categoría no encontrada"}}
            },
        }
    },
)
def ver_categoria(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    categoria_obtenida = db.get(Category, id)

    if not categoria_obtenida:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    return categoria_obtenida


# AGREGAR CATEGORIA
@categories_router.post("/", tags=["Categorías"], response_model=CategoryRead)
def agregar_categoria(categoria: CategoryCreate, db: Session = Depends(get_db)):
    nueva_categoria = Category.model_validate(categoria)

    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)

    return nueva_categoria


# REESCRIBIR CATEGORIA
@categories_router.put(
    "/{id}",
    tags=["Categorías"],
    response_model=CategoryRead,
    responses={
        404: {
            "description": "Categoría no encontrada",
            "content": {
                "application/json": {"example": {"detail": "Categoría no encontrada"}}
            },
        }
    },
)
def reescribir_categoria(
    id: Annotated[int, Path(gt=0)],
    categoria: CategoryCreate,
    db: Session = Depends(get_db),
):
    categoria_obtenida = db.get(Category, id)

    if not categoria_obtenida:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    categoria_obtenida.name = categoria.name

    db.commit()
    db.refresh(categoria_obtenida)

    return categoria_obtenida


# BORRAR CATEGORIA
@categories_router.delete(
    "/{id}",
    tags=["Categorías"],
    response_model=list[CategoryRead],
    responses={
        404: {
            "description": "Categoría no encontrada",
            "content": {
                "application/json": {"example": {"detail": "Categoría no encontrada"}}
            },
        }
    },
)
def borrar_categoria(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    categoria_obtenida = db.get(Category, id)

    if not categoria_obtenida:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(categoria_obtenida)
    db.commit()

    return db.exec(select(Category)).all()
