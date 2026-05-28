#!/usr/bin/python3

from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth import verify_token

security=HTTPBearer()

def get_db():

    db = SessionLocal()
    
    try:
        yield db 

    finally:
        db.close()

async def get_current_user( 
                           credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    email = verify_token(token)
    
    return email

