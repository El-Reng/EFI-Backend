from sqlmodel import Field, Relationship, SQLModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    is_owner: bool = False


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    modified_products: list["Product"] = Relationship(back_populates="last_modified_by")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int