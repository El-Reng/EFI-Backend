from fastapi import HTTPException, Path, APIRouter, Depends
from typing import Annotated
from ..database import get_db
from sqlmodel import Session, select
from ..models import (
    Product,
    ProductCreate,
    ProductRead,
)

products_router = APIRouter()


# PRODUCTS
@products_router.get("/", tags=["Productos"], response_model=list[ProductRead])
def ver_productos(db: Session = Depends(get_db)):
    return db.exec(select(Product)).all()


# PRODUCT
@products_router.get(
    "/{id}",
    tags=["Productos"],
    response_model=ProductRead,
    responses={
        404: {
            "description": "Producto no encontrado",
            "content": {
                "application/json": {"example": {"detail": "Producto no encontrado"}}
            },
        }
    },
)
def ver_producto(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    producto_obtenido = db.get(Product, id)

    if not producto_obtenido:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto_obtenido


# AGREGAR PRODUCTO
@products_router.post("/", tags=["Productos"], response_model=ProductRead)
def agregar_producto(producto: ProductCreate, db: Session = Depends(get_db)):
    nuevo_producto = Product.model_validate(producto)

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto


# REESCRIBIR PRODUCTO
@products_router.put(
    "/{id}",
    tags=["Productos"],
    response_model=ProductRead,
    responses={
        404: {
            "description": "Producto no encontrado",
            "content": {
                "application/json": {"example": {"detail": "Producto no encontrado"}}
            },
        }
    },
)
def reescribir_producto(
    id: Annotated[int, Path(gt=0)],
    producto: ProductCreate,
    db: Session = Depends(get_db),
):
    producto_obtenido = db.get(Product, id)

    if not producto_obtenido:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto_obtenido.name = producto.name
    producto_obtenido.description = producto.description
    producto_obtenido.price = producto.price
    producto_obtenido.category_id = producto.category_id
    producto_obtenido.last_modified_by_user_id = producto.last_modified_by_user_id

    db.commit()
    db.refresh(producto_obtenido)

    return producto_obtenido


# BORRAR PRODUCTO
@products_router.delete(
    "/{id}",
    tags=["Productos"],
    response_model=list[ProductRead],
    responses={
        404: {
            "description": "Producto no encontrado",
            "content": {
                "application/json": {"example": {"detail": "Producto no encontrado"}}
            },
        }
    },
)
def borrar_producto(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    producto_obtenido = db.get(Product, id)

    if not producto_obtenido:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto_obtenido)
    db.commit()

    return db.exec(select(Product)).all()
