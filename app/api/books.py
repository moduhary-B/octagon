from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas import BookCreate, BookUpdate, BookResponse
from app.db.db import get_db
from app.db.crud import (
    get_all_books,
    get_book,
    get_books_by_category,
    create_book,
    update_book,
    delete_book,
    get_category,
)

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse])
def list_books(
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    if category_id is not None:
        return get_books_by_category(db, category_id)
    return get_all_books(db)


@router.get("/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookResponse, status_code=201)
def create_new_book(data: BookCreate, db: Session = Depends(get_db)):
    if data.category_id is not None:
        category = get_category(db, data.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    book = create_book(
        db,
        title=data.title,
        description=data.description,
        price=data.price,
        url=data.url,
        category_id=data.category_id,
    )
    if not book:
        raise HTTPException(status_code=400, detail="Failed to create book")
    return get_book(db, book.id)


@router.put("/{book_id}", response_model=BookResponse)
def update_existing_book(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_db),
):
    existing = get_book(db, book_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    if data.category_id is not None:
        category = get_category(db, data.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    book = update_book(
        db,
        book_id,
        title=data.title,
        description=data.description,
        price=data.price,
        url=data.url,
        category_id=data.category_id,
    )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=204)
def delete_existing_book(book_id: int, db: Session = Depends(get_db)):
    success = delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
