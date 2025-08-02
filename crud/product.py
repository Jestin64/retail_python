# crud/product.py
from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, data: ProductCreate) -> Product:
    prod = Product(**data.dict())
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod

def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(
    db: Session,
    product_id: int,
    data: ProductUpdate,
) -> Product | None:
    prod = get_product(db, product_id)
    if not prod:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(prod, field, value)

    db.commit()
    db.refresh(prod)
    return prod

def delete_product(db: Session, product_id: int) -> bool:
    prod = get_product(db, product_id)
    if not prod:
        return False

    db.delete(prod)
    db.commit()
    return True

    return False
