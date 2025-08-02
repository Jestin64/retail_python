from sqlalchemy.orm import Session
from models.category import Category
from schemas.category import CategoryCreate

def create_category(db: Session, cat_in: CategoryCreate) -> Category:
    db_cat = Category(**cat_in.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, cat_in: CategoryCreate) -> Category | None:
    db_cat = get_category(db, category_id)
    if db_cat:
        db_cat.name = cat_in.name
        db.commit()
        db.refresh(db_cat)
    return db_cat

def delete_category(db: Session, category_id: int) -> bool:
    db_cat = get_category(db, category_id)
    if db_cat:
        db.delete(db_cat)
        db.commit()
        return True
    return False
