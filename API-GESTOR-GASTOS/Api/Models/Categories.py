from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP, DateTime,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from Api.Models.base_class import Base




class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, autoincrement=True, primary_key=True)
    category_name = Column(String(50), nullable=False)
    category_description = Column(String(120), nullable=False)
    category_status = Column(Boolean, default=True)

    transactions = relationship("Transaction",back_populates="category")

 