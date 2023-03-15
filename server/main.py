from fastapi import FastAPI, UploadFile, File
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
import os
from PIL import Image
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi_jwt_auth import AuthJWT
from routers import user,image
import schemas,models

app = FastAPI(title="Image server")

class Settings(schemas.BaseModel):
    authjwt_secret_key: str = "mysuperkey"

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(user.router)
app.include_router(image.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)