from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP, DateTime,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from datetime import datetime
from Api.Models.transacciones import Transaction
from Api.Models.base_class import Base
from Api.Models.tokens import Token_Model


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(30), primary_key=True)
    full_name = Column(String(80), nullable=False)
    mail = Column(String(100), unique=True, nullable=False)
    passhash = Column(String(140), nullable=False)
    user_role = Column(Enum('admin', 'user'), nullable=False)
    user_status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = relationship("Transaction",back_populates="user")
    tokens = relationship("Token_Model",back_populates="user")


