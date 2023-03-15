
from fastapi import APIRouter,Depends,HTTPException,File,UploadFile
from fastapi.security import APIKeyHeader, APIKeyQuery
from datetime import datetime, timedelta
from auth.bearer import JWTBearer
from sqlalchemy.orm import Session
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.exc import IntegrityError
from fastapi_jwt_auth import AuthJWT
from models import engine
import schemas,models
from PIL import Image
import os

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/image",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def default():
    return [{"id":1,"product": "Laptop"}, {"id":2,"product": "Mobile"}]

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
        
    # Open the image file and resize it to generate a thumbnail
    with Image.open(file_location) as image:
        thumbnail_size = (128, 128)
        image.thumbnail(thumbnail_size)
        thumbnail_location = f"temp/thumbnail-{file.filename}"
        image.save(thumbnail_location)
        
    # Remove the temporary files
    os.remove(file_location)
    
    # Return the location of the thumbnail
    return {"thumbnail_location": thumbnail_location}
