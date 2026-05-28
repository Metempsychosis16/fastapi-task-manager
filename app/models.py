#!/usr/bin/python3


from pydantic import BaseModel,Field,EmailStr
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column,String,Boolean,ForeignKey
from app.database import Base

class TaskDB(Base):
    __tablename__="tasks"

    id=Column(String,primary_key=True,default=lambda:str(uuid4()))
    title=Column(String)
    description=Column(String)
    completed=Column(Boolean,default=False)
    owner_email=Column(String,ForeignKey("users.email"))


class TaskCreate(BaseModel):

    title:str=Field(min_length=3)
    description:str=Field(min_length=5)
    completed:bool=False

class TaskUpdate(BaseModel):

    title: Optional[str]=None
    description :Optional [str]=None
    completed:Optional[bool]=None

class TaskResponse(BaseModel):

    id:UUID
    title:str
    description:str
    completed:bool

class UserCreate(BaseModel):
    email:EmailStr
    password:str

    model_config={  
                  "json_schema_extra": {
                      "example":{
                      "email":"test@gmail.com",
                      "password":"123456"
                      } 
                 }
            }


            

class UserResponse(BaseModel):
    id:str
    email:EmailStr

class UserDB(Base):
    __tablename__="users"
    id=Column(String,primary_key=True,default=lambda:str(uuid4()))
    email=Column(String,unique=True)
    password=Column(String)
class SortOrder(str,Enum):
    asc="asc"
    desc="desc"
class MessageResponse(BaseModel):
    message:str
