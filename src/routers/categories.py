from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_db
from ..models import Category, CategoryCreate, CategoryRead

# Router sin prefijo; se agrega al incluir en ``main``
router = APIRouter(prefix="/categories")


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Categorías"],
)
def crear_categoria(categoria: CategoryCreate, db: Session = Depends(get_db)):
    db_categoria = Category.from_orm(categoria)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@router.get("/", response_model=list[CategoryRead], tags=["Categorías"])
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorias = db.exec(select(Category).offset(skip).limit(limit)).all()
    return categorias


@router.get("/{category_id}", response_model=CategoryRead, tags=["Categorías"])
def obtener_categoria(category_id: int, db: Session = Depends(get_db)):
    categoria = db.get(Category, category_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.put("/{category_id}", response_model=CategoryRead, tags=["Categorías"])
def actualizar_categoria(
    category_id: int, categoria_update: CategoryCreate, db: Session = Depends(get_db)
):
    categoria = db.get(Category, category_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    datos = categoria_update.dict()
    for key, value in datos.items():
        setattr(categoria, key, value)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


@router.delete(
    "/{category_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Categorías"]
)
def borrar_categoria(category_id: int, db: Session = Depends(get_db)):
    categoria = db.get(Category, category_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria)
    db.commit()
    return None
