"""Modelos de categoría para el backend de la panadería.

Este módulo define la tabla ``Category`` y los esquemas de creación/lectura.
"""

from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .product import Product


class CategoryBase(SQLModel):
    """Campos comunes para crear o leer categorías."""

    name: str = Field(index=True, unique=True)


class Category(CategoryBase, table=True):
    """Modelo de tabla ``category``.

    Relación inversa con los productos que pertenecen a la categoría.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["Product"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    """Esquema usado al crear o actualizar una categoría vía la API."""

    pass


class CategoryRead(CategoryBase):
    """Esquema que devuelve la API (incluye el id)."""

    id: int
