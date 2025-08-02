from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class Product(Base):
    __tablename__ = "products"
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    price       = Column(Float, nullable=False)
    stock       = Column(Integer, nullable=False, default=0)
    # 1️⃣ ForeignKey ties this column to categories.id
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # 2️⃣ relationship tells SQLAlchemy how to load the Category object
    category = relationship("Category", back_populates="products")
