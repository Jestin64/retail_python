print("🔍 product.py is loading")

from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate

# CREATE
def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# READ (single)
def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()

# READ (all)
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

# UPDATE
def update_product(db: Session, product_id: int, data: ProductCreate) -> Product | None:
    db_product = get_product(db, product_id)
    if db_product:
        for field, value in data.dict().items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product

# DELETE
def delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
