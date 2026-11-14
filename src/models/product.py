from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from datetime import datetime, timezone

from .category import CategoryPublic
from .user import UserPublic

if TYPE_CHECKING:
    from .category import Category
    from .user import User


class ProductBase(SQLModel):
    name: str = Field(min_length=1)
    description: str | None = None
    price: float = Field(gt=0)


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id")
    last_modified_by_user_id: int = Field(foreign_key="user.id")
    last_modified_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    category: "Category" = Relationship(back_populates="products")
    last_modified_by: "User" = Relationship(back_populates="modified_products")


class ProductCreate(ProductBase):
    category_id: int
    last_modified_by_user_id: int


class ProductPublic(ProductBase):
    id: int


class ProductPublicNested(ProductPublic):
    category: CategoryPublic
    last_modified_by: UserPublic
    last_modified_at: datetime
