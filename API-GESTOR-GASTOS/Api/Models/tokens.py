# from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP, DateTime,Boolean,ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.mysql import TINYINT
# from Api.Models.base_class import Base
# from datetime import datetime
# from Api.Models.User import User




# class Token_Model(Base):
#     __tablename__ = "tokens"

#     token = Column(String(100), primary_key=True)
#     user_id = Column(String(30),ForeignKey('users.user_id'))
#     token_status = Column(Boolean, default=True)
#     token_created_at = Column(TIMESTAMP, default=datetime.utcnow)

#     user = relationship("User",back_populates="tokens")

 