from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .category import Category
    from .user import User

# Runtime imports for nested read models
from .category import CategoryRead
from .user import UserRead


class ProductBase(SQLModel):
    name: str
    description: Optional[str] = None
    price: float


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id")
    last_modified_by_user_id: int = Field(foreign_key="user.id")
    category: "Category" = Relationship(back_populates="products")
    created_by: "User" = Relationship(back_populates="created_products")


class ProductCreate(ProductBase):
    category_id: int
    last_modified_by_user_id: int


class ProductRead(ProductBase):
    id: int
    category: "CategoryRead"
    created_by: "UserRead"
