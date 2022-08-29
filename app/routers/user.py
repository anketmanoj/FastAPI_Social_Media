from fastapi import Response
from fastapi import status
from fastapi import HTTPException, Depends, APIRouter
from .. import models, schema
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, response: Response, db: Session = Depends(get_db)):
    userCheckQuery = db.query(models.Users).filter(models.Users.email == user.email).first()
    if userCheckQuery:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail={"Error": "User already exists"})
    user.password = utils.hash(user.password)
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response.status_code = status.HTTP_201_CREATED
    return new_user

@router.get("/id:{id}", response_model=schema.UserResponse)
def get_one_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"Error" : "User not found"})
    
    return user
