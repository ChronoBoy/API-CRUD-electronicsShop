from typing import Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import RollbackToSavepointClause
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from fastapi.responses import JSONResponse

from .dbConnect import SessionLocal, engine

from . import models, schemas


db = SessionLocal()

def get_user(db: Session,user_id:int):
    
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_name(db: Session, name:str):
    return db.query(models.User).filter(models.User.name == name).first()    

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session,offset: int = 0, limit: int = 2):

    stmt = select(models.User).offset(offset).limit(limit)
    result = db.execute(stmt).scalars().all()

    # print("Primera forma: ",db.query(models.User).offset(offset).limit(limit).all())
    # print("Segunda forma:")
    # print("con scalars: ", db.execute(stmt).scalars().all())
    # print("sin scalars: ", db.execute(stmt).all())
    
    return result


def create_user(db: Session, user: schemas.UserCreate, item: schemas.ItemCreate):
    
    fake_hashed_password = user.password + "nothashed"
    db_user = models.User(email = user.email, 
    password = fake_hashed_password,name = user.name,
    lastname = user.lastname,age=user.age)

   
    try:
        db.add(db_user)
        print("aqui")
        db.commit()
        print (db_user.user_id)
    except Exception as e:
        print("Error")
        print (e)
        db.rollback()
        db.flush()
        return {"Error": "ROLLBACK STATEMENT"}       
          
    else:

        db_user_item = models.Item(**item.dict(), item_owner =  db_user.user_id)
        db.add(db_user_item)
        db.commit()
        return db.query(models.User).filter(models.User.user_id == db_user.user_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 2):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), item_owner =  user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item 

def update_user_info(db: Session,user_id: int, name: str, lastname: str, age: int, email: str, password: str, is_active: bool):
    query = db.query(models.User).filter(models.User.user_id == user_id).first()

    if name == None:
        
        name = query.name

    if lastname == None:
        
        lastname = query.lastname

    if age == None:
        
        age = query.age

    if email == None:
       
        email = query.email

    if password == None:
       
        password = query.password

    if is_active == None:
       
        is_active = query.is_active 


    db_update = db.query(models.User).filter(models.User.user_id == user_id).update(
    {models.User.name:name, models.User.lastname:lastname,models.User.age:age,models.User.email:email,
    models.User.password:password,models.User.is_active:is_active}, 
    synchronize_session=False)
    db.commit()
    return db_update 


def count_items(db: Session,user_id: int):
    return db.query(models.Item).filter(models.Item.item_owner == user_id).count()

def update_user_items(db: Session, item_id: int, item_name: str, item_description: str):
    query = db.query(models.Item).filter(models.Item.item_id == item_id).first()

    if item_name != None:
        
        query.item_name = item_name

    if item_description != None:
        
        query.item_description = item_description

    db.commit()
    return query  


def update_pic(db: Session,user_id: int, image_name: str):
    query = db.query(models.User).filter(models.User.user_id == user_id).first()
    query.img_prf = image_name
    db.commit()
    return query.img_prf

def get_pic_info(db: Session, url_image: str):
    query_getImgInfo = db.query(models.User).filter(models.User.img_prf == url_image).first()
    return query_getImgInfo.img_prf




