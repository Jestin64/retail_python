from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.product import ProductCreate, ProductOut
from crud.product import(
    create_product,
    get_product,
    get_products,
    update_product,
    delete_product
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.get("/", response_model=list[ProductOut])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products(db, skip, limit)

@router.get("/{product_id}", response_model=ProductOut)
def read_one(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    updated = update_product(db, product_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(product_id: int, db: Session = Depends(get_db)):
    if not delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
