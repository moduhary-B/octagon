from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from app.db.db import get_db
from app.db.crud import (
    get_all_categories,
    get_category,
    create_category,
    update_category,
    delete_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_new_category(data: CategoryCreate, db: Session = Depends(get_db)):
    category = create_category(db, data.title)
    if not category:
        raise HTTPException(status_code=400, detail="Failed to create category")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_existing_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = update_category(db, category_id, data.title)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}", status_code=204)
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    success = delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
