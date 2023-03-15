
from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import APIKeyHeader, APIKeyQuery
from datetime import datetime, timedelta
from auth.bearer import JWTBearer
from sqlalchemy.orm import Session
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.exc import IntegrityError
from fastapi_jwt_auth import AuthJWT
from models import engine
import schemas,models

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/user",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def default():
    return [{"id":1,"product": "Laptop"}, {"id":2,"product": "Mobile"}]

@router.post("/register")
async def register(user:schemas.UserBase,Authorize: AuthJWT = Depends(),db: Session = Depends(get_db)):
    datam = {'email':user.email}
    try:
        db_user = models.User(email=user.email)
        db.add(db_user)
        db.commit()
        access_token = Authorize.create_access_token(subject=str(datam),expires_time=60000)
        return {"access_token": access_token}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="email is already exist")

