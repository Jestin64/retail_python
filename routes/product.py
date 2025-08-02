# routes/product.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from schemas.product import ProductCreate, ProductUpdate, ProductOut
from crud.product import (
    create_product,
    get_product,
    get_products,
    update_product,
    delete_product,
)
from db.session import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductOut])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_products(db, skip, limit)

@router.get("/{product_id}", response_model=ProductOut)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    prod = get_product(db, product_id)
    if not prod:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return prod

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(
    payload: ProductCreate,
    db: Session = Depends(get_db),
):
    return create_product(db, payload)

@router.put("/{product_id}", response_model=ProductOut)
def update_product_endpoint(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
):
    updated = update_product(db, product_id, payload)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
