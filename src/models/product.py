
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from datetime import datetime

from .category import CategoryRead
from .user import UserRead

if TYPE_CHECKING:
    from .category import Category
    from .user import User


class ProductBase(SQLModel):
    name: str
    description: str | None = None
    price: float


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id")
    last_modified_by_user_id: int = Field(foreign_key="user.id")
    last_modified_at: datetime = Field(default_factory=datetime.utcnow)

    category: "Category" = Relationship(back_populates="products")
    last_modified_by: "User" = Relationship(back_populates="modified_products")


class ProductCreate(ProductBase):
    category_id: int
    last_modified_by_user_id: int


class ProductRead(ProductBase):
    id: int
    category: CategoryRead
    last_modified_by: UserRead
    last_modified_at: datetime
