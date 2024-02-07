from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP, DateTime,Boolean
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

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
