from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_db
from ..models import Product, ProductCreate, ProductRead, CategoryRead, UserRead

# Router sin prefijo; se agrega al incluir en ``main``
router = APIRouter()


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Productos"],
)
def crear_producto(producto: ProductCreate, db: Session = Depends(get_db)):
    db_producto = Product.from_orm(producto)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


@router.get("/", response_model=list[ProductRead], tags=["Productos"])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = db.exec(select(Product).offset(skip).limit(limit)).all()
    return productos


@router.get("/{product_id}", response_model=ProductRead, tags=["Productos"])
def obtener_producto(product_id: int, db: Session = Depends(get_db)):
    producto = db.get(Product, product_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{product_id}", response_model=ProductRead, tags=["Productos"])
def actualizar_producto(
    product_id: int, producto_update: ProductCreate, db: Session = Depends(get_db)
):
    producto = db.get(Product, product_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    datos = producto_update.dict()
    for key, value in datos.items():
        setattr(producto, key, value)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Productos"]
)
def borrar_producto(product_id: int, db: Session = Depends(get_db)):
    producto = db.get(Product, product_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return None
