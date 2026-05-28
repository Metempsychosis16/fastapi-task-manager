#!/usr/bin/python3

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta,UTC
from fastapi import HTTPException
from app.config import (SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES)



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return email

    except JWTError as e:

        print(e)

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
