from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.category import CategoryCreate, CategoryOut
from crud.category import (
    create_category,
    get_category,
    get_categories,
    update_category,
    delete_category,
)
from core.security import get_current_user, admin_required
from models.user import User
from db.session import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

# List all categories (any logged‑in user)
@router.get("/", response_model=list[CategoryOut])
def list_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_categories(db, skip, limit)

# Get one category by ID (any logged‑in user)
@router.get("/{category_id}", response_model=CategoryOut)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    cat = get_category(db, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

# Create a category (admins only)
@router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
)
def create_category_endpoint(
    cat_in: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
):
    return create_category(db, cat_in)

# Update a category (admins only)
@router.put("/{category_id}", response_model=CategoryOut)
def update_category_endpoint(
    category_id: int,
    cat_in: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
):
    updated = update_category(db, category_id, cat_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

# Delete a category (admins only)
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
):
    success = delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return
