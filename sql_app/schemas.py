from pydantic import BaseModel

from typing import List,Optional


class ItemBase(BaseModel):
    item_name: str
    item_description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    item_id: int
    item_owner: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: str
    lastname: str
    age: Optional [int] = None
    img_prf: Optional[str] = None

class UserCreate(UserBase):
    password: str    


class User(UserBase):
    user_id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode=True




