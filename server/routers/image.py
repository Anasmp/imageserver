
from fastapi import APIRouter,Depends,HTTPException,File,UploadFile
from fastapi.responses import FileResponse
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
import random
from resizeimage import resizeimage

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

@router.post("/upload-image",dependencies=[Depends(JWTBearer())])
async def upload_image(file: UploadFile = File(...),thumbnail_size: int = 128,db: Session = Depends(get_db),authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    randomkey = ''.join(random.choice('0123456789') for i in range(15))

    file_location = f"storage/{file.filename}"
    filename,file_extension = os.path.splitext(file.filename)
    newpath = f"storage/{randomkey}{file_extension}"
    bfpath = f"{randomkey}{file_extension}"

    with open(newpath, "wb") as buffer:
        buffer.write(file.file.read())

    db_image = models.Images(user_id=eval(current_user)['userid'],image=bfpath)
    db.add(db_image)
    db.commit()
    return {"message": "Images uploaded successfully"}


@router.get("/my-images",dependencies=[Depends(JWTBearer())])
async def default(db: Session = Depends(get_db),authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    db_images =  db.query(models.Images).filter(models.Images.user_id == eval(current_user)['userid']).all()
    return db_images

@router.get("/{filename}")
async def read_image(filename: str, width: int = 0):
    image_path = f"storage/{filename}"
    thumbnail_path = f"thumb/{width}/{filename}"

    if width:
        if os.path.isfile(thumbnail_path):
            # Return the cached thumbnail if it already exists
            return FileResponse(thumbnail_path)

        if os.path.isfile(image_path):
            # Generate the thumbnail from the original image
            with Image.open(image_path) as image:
                thumbnail = resizeimage.resize_width(image, width, validate=False)
                os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
                thumbnail.save(thumbnail_path, image.format)

            # Return the newly generated thumbnail
            return FileResponse(thumbnail_path)
    else:
        return FileResponse(image_path)

    # Return a 404 Not Found response if the image file doesn't exist
    raise HTTPException(status_code=404, detail="Image not found")

