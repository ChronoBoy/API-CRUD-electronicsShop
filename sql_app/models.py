from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from sqlalchemy.orm import relationship
from .dbConnect import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean,default=True)
    img_prf = Column(String, unique=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer,primary_key=True)
    item_name = Column(String)
    item_description = Column(String)
    item_owner = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="items")



