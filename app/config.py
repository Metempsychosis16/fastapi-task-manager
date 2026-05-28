#!/usr/bin/python3

import os 
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
DATABASE_URL=os.getenv("DATABASE_URL")  
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",60))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY missing")
