from typing import List,Optional

from fastapi import Depends, FastAPI, HTTPException,File,UploadFile,Request
from fastapi.param_functions import Path
from fastapi.responses import Response,FileResponse,JSONResponse
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from . import crud, models, schemas
from .dbConnect import SessionLocal, engine
import uuid
import os
import shutil




models.Base.metadata.create_all(bind=engine)

description = """

The best service for your electronic devices in the world

## Users

You can create users and read their information

## Items

The electronic device that the user is going to leave in the building

"""


class CustomExceptionEmail(Exception):
    def __init__(self,dbEmail):
        self.dbEmail = dbEmail
        

class CustomExceptionName(Exception):
    def __init__(self,dbName):
        self.dbName = dbName        

app = FastAPI(
    title="TechFixApp",
    description=description,
    version = "0.0.1",
    contact = {
        "name": "Alvaro Juarez",
        "url": "http://contact.com",
        "email": "ajuhez@gmail.com"
    })

app.mount("/static", StaticFiles(directory="static"), name = "static")    


@app.exception_handler(CustomExceptionEmail)
async def emailExists(request: Request, exc: CustomExceptionEmail):
    return JSONResponse(
        status_code=400,
        content = {"Error message": f"The email {exc.dbEmail} has already registered, please choose another one"}
    )

@app.exception_handler(CustomExceptionName)
async def nameExists(request: Request, exc: CustomExceptionName):
    return JSONResponse(
        status_code=400,
        content = {"Error message": f"The name {exc.dbName} has already registered, please choose another one"}
    )    

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise     
    finally:
        db.close()


user_name = "Alvaro_juarez"
static = f"{os.getcwd()}/static"



@app.get("/images/{file_name}")
async def main(file_name: str ):
    return FileResponse(os.path.join(static, file_name))

@app.post("/images/{user_id}") 
async def create_upload_file(user_id: int,image: UploadFile = File(...),db: Session = Depends(get_db)):

    
    image.filename = f"{user_name}_prfp.jpg"
    local_url = f"static/{image.filename}"
    update_pic = crud.update_pic(user_id=user_id,db=db,image_name = image.filename)

    with open(local_url, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return update_pic 


@app.post("/users/",summary="Create user", description="Create a new user for future actions", response_model=schemas.User)
def create_user(user:schemas.UserCreate,item: schemas.ItemCreate ,db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    db_user_name = crud.get_name(db, name=user.name)


    if db_user:
        raise CustomExceptionEmail(dbEmail=db_user.email)  

    if db_user_name:

        raise CustomExceptionName(dbName=db_user_name.name) 
        
    return crud.create_user(db=db, user=user, item=item)

@app.get("/users/", response_model=List[schemas.User],summary="Read all users", description="Filter by offset and limit the number of users you want to see")
def read_users(offset: int = 0, limit: int = 2,db:Session = Depends(get_db)):
    users = crud.get_users(offset=offset, limit=limit, db=db)
    return users
   

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return db_user


@app.post("/users/{user_id}/items", response_model= schemas.Item)
def create_item_for_user(user_id: int, item:schemas.ItemCreate, db: Session = Depends(get_db)):
    count_items = crud.count_items(user_id=user_id, db=db)
    if count_items >= 3:
        raise HTTPException(status_code = 400, detail = "You cant put more than 3 active items per user")

    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model = List[schemas.Item])
def read_items(skip: int = 0, limit: int = 2, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.put("/users/{user_id}")
def update_user_info(user_id:int, name: Optional[str] = None, 
lastname: Optional[str] = None,
age: Optional[str] = None, email: Optional[str] = None,password: Optional[str] = None,is_active: Optional[bool] = None, db:Session = Depends(get_db)):
     update_user = crud.update_user_info(user_id=user_id, name=name, db=db, lastname=lastname, age=age,
     email=email,password = password, is_active=is_active)
     return update_user


@app.put("/items/{item_id}")
def update_user_items(*,item_name: Optional[str] = None,item_description: Optional[str] = None,item_id: int, db:Session = Depends(get_db)):
     update_user_item = crud.update_user_items(item_id=item_id, db=db, item_name=item_name, item_description=item_description)
     return update_user_item     

  
    






