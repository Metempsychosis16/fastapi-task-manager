#!/usr/bin/python3


from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from uuid import uuid4
from sqlalchemy import desc


from app.models import TaskDB,TaskCreate,TaskUpdate,TaskResponse,UserCreate,UserResponse,UserDB,SortOrder,MessageResponse
from app.auth import hash_password,verify_password,create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import verify_token
from app.dependencies import get_db,get_current_user
from fastapi import UploadFile,File
import shutil
import os


router=APIRouter()





@router.get("/protected")
async def protected_route(current_user:str = Depends(get_current_user)):
    return{
            "message":"Protected route accessed",
            "user":current_user

            }


@router.post("/tasks",response_model=TaskResponse)
async def create_task(task:TaskCreate,current_user:str=Depends(get_current_user),db:Session=Depends(get_db)):
    db_task=TaskDB(title=task.title,description=task.description,completed=task.completed,owner_email=current_user)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks",tags=["Tasks"],response_model=list[TaskResponse])



async def get_taskdb(skip:int=0,limit:int=10,q:str|None=None,completed:bool|None=None,sort:SortOrder=SortOrder.asc ,current_user:str=Depends(get_current_user),db:Session=Depends(get_db)):


    query=db.query(TaskDB).filter(TaskDB.owner_email==current_user)



    if q:
        query=query.filter(TaskDB.title.contains(q))

    if completed is not None:
        query=query.filter(TaskDB.completed==completed)

    if sort==SortOrder.desc:
        query=query.order_by(desc(TaskDB.title))
    else:
        query=query.order_by(TaskDB.title)

    tasks=query.offset(skip).limit(limit).all()

        
    return tasks

@router.get("/tasks/{task_id}",response_model=TaskResponse)

async def get_task(task_id:str,current_user:str=Depends(get_current_user),db:Session=Depends(get_db)):
    task=db.query(TaskDB).filter(TaskDB.id==task_id,TaskDB.owner_email==current_user).first()
   
    if not task:
        raise HTTPException(status_code=404,detail="task not found")

    return task
   



@router.put("/tasks/{task_id}",response_model=TaskResponse)
async def update_task(task_id:str,updated:TaskUpdate,current_user:str=Depends(get_current_user),db:Session=Depends(get_db)):
    task= db.query(TaskDB).filter(TaskDB.id==task_id,TaskDB.owner_email==current_user).first()

    if not task:
        raise HTTPException(status_code=404,detail="Task not found")

    

    if updated.title is not None:
        task.title=updated.title
    if updated.description is not None:
        task.description=updated.description
    if updated.title is not None:
        task.completed=updated.completed
    db.commit()
    db.refresh(task)
    return task
    

@router.delete("/tasks/{task_id}",response_model=MessageResponse,tags=["Delete Task"],summary="Delete a user",description="Delete a user with id",status_code=status.HTTP_200_OK)

async def delete_task(task_id:str,current_user:str=Depends(get_current_user),db:Session=Depends(get_db)):

    task=db.query(TaskDB).filter(TaskDB.id==task_id,TaskDB.owner_email==current_user).first()
    
    if not task:
        raise HTTPException(status_code=404,detail="task not found")

    db.delete(task)
    db.commit()
    
    return MessageResponse(message="Task Deleted")


@router.post("/register",tags=["Authentication"],summary="Register a new user",description="Creates a new account with hased password",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate,db:Session=Depends(get_db)):
    
    existing_user= db.query(UserDB).filter(UserDB.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already exists")

    db_user=UserDB(email=user.email,password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@router.post("/login",tags=["Login"],summary="User Login",status_code=status.HTTP_200_OK)

async def login(user:UserCreate,db:Session=Depends(get_db)):
    db_user=db.query(UserDB).filter(UserDB.email==user.email).first()
    if not db_user:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    if not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=401,detail="Invalid Credentials")

    token=create_access_token({"sub":db_user.email})
    return {"access_token":token}


UPLOAD_DIR="app/uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

@router.post("/upload",tags=["Upload Files"])
async def upload_file(file:UploadFile=File(...),current_user:str=Depends(get_current_user),db:Session=Depends(get_db)):
    task=db.query(TaskDB).filter(TaskDB.owner_email==current_user).first()
    
    unique_name=f"{uuid4()}_{file.filename}"
    

    file_path=f"{UPLOAD_DIR}/{unique_name}"
        

    

    with open (file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    return{
            "filename":unique_name,
            "url":f"/uploads/{unique_name}"
            }



