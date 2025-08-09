from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from crud.category import (
    create_category,
    get_category,
    get_categories,
    update_category,
    delete_category,
)
from db.session import get_db
from core.security import get_current_user, admin_required
from models.user import User

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryOut])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)  # Authenticated users can read categories
):
    return get_categories(db, skip, limit)

@router.get("/{category_id}", response_model=CategoryOut)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category_endpoint(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required)  # Admin only
):
    return create_category(db, payload)

@router.put("/{category_id}", response_model=CategoryOut)
def update_category_endpoint(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required)  # Admin only
):
    updated = update_category(db, category_id, payload)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
    return updated

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required)  # Admin only
):
    success = delete_category(db, category_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")

