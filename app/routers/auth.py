from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from .. import models, schema
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth2


router = APIRouter(
    tags=['Auth']
) 

@router.post("/login", response_model=schema.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"Error" : "Email does not match any user"})
    verifyPassword = utils.verify(user_credentials.password, user.password)
    if not verifyPassword:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"Error" : "Incorrect Credentials"})
    
    #* Create JWT Token
    #* return Token

    accessToken = oauth2.create_access_token(data={"user_id" : user.id})
    return {"access_token" : accessToken, "token_type" : "bearer"}
    

