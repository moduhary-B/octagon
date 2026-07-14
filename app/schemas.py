from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: str


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: Optional[Decimal] = None
    url: Optional[str] = None
    category_id: Optional[int] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    url: Optional[str] = None
    category_id: Optional[int] = None


class BookResponse(BookBase):
    id: int
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True
