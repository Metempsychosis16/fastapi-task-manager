#!/usr/bin/python3

from fastapi import FastAPI
from app.database import engine,Base
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
app=FastAPI(title="Task Manager API",description="A Modern FastAPI Backend  With JWT Authentitcation And Task Management ", version="1.0.0")



@app.get("/")
async def home():

    return {
        "message": "FastAPI Task Manager API is running",
        "docs": "/docs"
    }

#middleware
app.add_middleware(

        CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])



@app.middleware("http")
async def log_request(request:Request,call_next):
    start_time=time.time()

    response=await call_next(request)
    process_time=time.time() - start_time
    response.headers["X-Process-Time"]=str(process_time)

    print(f"{request.method} {request.url} completed in {process_time:.4f}s")
    
    return response


                
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request,exc):
    return JSONResponse(status_code=422,content={"message":"Invalid input","details":exc.errors()})

@app.get("/health")
async def health():
    return {"status":"running"}

#staticfiles

app.mount("/uploads",StaticFiles(directory="app/uploads"),name="upload")

#database

Base.metadata.create_all(bind=engine)


#routes
app.include_router(router,prefix="/api")
