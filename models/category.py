from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base

class Category(Base):
    __tablename__ = "categories"            # 1️⃣ This will create a table named "categories"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # 2️⃣ This sets up a bidirectional link to Product
    products = relationship("Product", back_populates="category")

