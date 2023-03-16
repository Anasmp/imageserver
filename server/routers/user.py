
from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import APIKeyHeader, APIKeyQuery
from datetime import datetime, timedelta
from auth.bearer import JWTBearer
from sqlalchemy.orm import Session
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.exc import IntegrityError
from auth.password import verify_password,get_password_hash
from sqlalchemy.exc import NoResultFound
from fastapi_jwt_auth import AuthJWT
from models import engine
import schemas,models
import re

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

def is_valid_email(email):
    """Return True if the email address is valid, False otherwise."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

@router.get("/")
async def default():
    return [{"id":1,"product": "Laptop"}, {"id":2,"product": "Mobile"}]

@router.post("/register")
async def register(user:schemas.UserBase,Authorize: AuthJWT = Depends(),db: Session = Depends(get_db)):
    
    if is_valid_email(user.email) and user.password:

        try:
            db_user = db.query(models.User).filter(models.User.email == user.email).one()
            if not verify_password(user.password,db_user.password):
                raise HTTPException(status_code=400, detail="Incorrect password")
            datam = {'email':db_user.email,"userid":db_user.id}
            access_token = Authorize.create_access_token(subject=str(datam),expires_time=60000)
            return {"access_token": access_token}
        except NoResultFound:
            hashpass=get_password_hash(user.password)
            db_user = models.User(email=user.email,password=hashpass)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            datam = {'email':user.email,"userid":db_user.id}
            access_token = Authorize.create_access_token(subject=str(datam),expires_time=60000)
            #send access register link to email
            return {"access_token": access_token}
    

        #     raise HTTPException(status_code=500, detail="email is already exist")
    else:

        raise HTTPException(status_code=500, detail="enter a valid mail or password")
