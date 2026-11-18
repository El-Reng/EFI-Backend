from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product


class UserBase(SQLModel):
    username: str = Field(min_length=1, index=True, unique=True)
    is_owner: bool = False


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    modified_products: list["Product"] = Relationship(back_populates="last_modified_by")


class UserCreate(SQLModel):
    username: str = Field(min_length=1)
    password: str
    is_owner: bool = False


class UserUpdateAdmin(SQLModel):
    username: str = Field(min_length=1)
    password: str | None = None
    is_owner: bool | None = None


class UserUpdateMe(SQLModel):
    current_password: str
    username: str | None = Field(default=None, min_length=1)
    password: str | None = None


class UserPublic(UserBase):
    id: int
