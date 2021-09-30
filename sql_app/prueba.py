from os import path
from fastapi import FastAPI,HTTPException,Path,Body
from fastapi.encoders import jsonable_encoder


from pydantic import BaseModel,EmailStr,Field,HttpUrl

from typing import List, Text,Optional

from datetime import datetime

from uuid import uuid4 as id

from enum import Enum

########################################



app = FastAPI()



userData = {
    "1": {"name": "Alvaro", "lastName" : "Juarez", "age": "27" },
    "2": {"name": "Astrid", "lastName" : "Chavez" } 
}

example = {"name": "Edoardo",
"lastName" : "Ruiz",
"age" : "24",
"tags":["C++", "C"],   
"image": {
    "url": "http://example.com/baz.jpg",
    "name": "myPic.png"
  }}


class UserImg(BaseModel):
    url: HttpUrl
    name: str 


class User(BaseModel):
   name: str 
   lastName: str
   age: Optional [int] = Field(..., title="The age is not important")
   tags: Optional [List[str]] = None
   image: Optional[UserImg] = None


class User_patch(BaseModel):
   name: Optional [str]
   lastName: Optional [str]
   age: Optional [int] = None
   image: Optional[UserImg] = None
 

@app.get("/user/")
async def getAllUsers():
    return userData 


@app.get("/user/{user_id}")
async def getAllUsersById(user_id: str = Path(..., description= "Pass the ID of the user to see specific info")):
    if user_id in userData.keys(): 
        return userData[user_id]
    return {"Error": "That ID does not exists"} 

   
@app.post("/create-user/{user_id}", response_model=User)
async def createUser(user_id: str = Path(...,description= "Put the ID for new user"), model: User = Body(...,example = example)):
    if user_id in userData.keys():
        return {"Error" : "That ID already exists"}
    userData[user_id] = model 
    return userData[user_id] 


@app.put("/update-all-user/{user_id}", response_model = User)
async def updateAllUser(user_id : str, model: User):
    if user_id not in userData.keys():
        return {"Error" : "That user does not exists, nothing to upgrade"}
    userData[user_id] = model
    return userData[user_id]
    

@app.patch("/update-data-user/{user_id}", response_model = User_patch)
async def updateDataUser(user_id: str, model: User_patch):
    if user_id not in userData.keys():
        return {"Error" : "That user does not exists, nothing to upgrade"}
    stored_user_data = userData[user_id]
    stored_item_model = User_patch(**stored_user_data)
    update_data = model.dict(exclude_unset=True)
    updated_itemOfUser = stored_item_model.copy(update=update_data)
    userData[user_id] = jsonable_encoder(updated_itemOfUser)
    return updated_itemOfUser

# @app.put("/add-data/{user_id}")
# async def addData(user_id: Optional [str] = Path(None,title= "The ID of the user to add data" ),
# tags: Optional [List[str]] = None):
#     if tags:
#         userData[user_id].update({"Tags" : tags})
#     return userData

@app.delete("/delete-data/{user_id}")
async def delData(user_id: str):
    if user_id not in userData.keys():
        return {"Error" : "That ID dos not exists, nothing to delete"}
    userData.pop(user_id)
    return userData    






   
        


    







    








