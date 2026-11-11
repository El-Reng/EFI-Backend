from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .product import Product


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    hashed_password: str
    is_owner: bool = False


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_products: List["Product"] = Relationship(back_populates="created_by")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
