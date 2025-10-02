# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from fastapi import APIRouter, status, Depends, HTTPException
# from typing import Annotated
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from models import Users
# from passlib.context import CryptContext
# from datetime import timedelta, timezone, datetime
# from jose import jwt, JWTError

# router = APIRouter(
#     tags=['Auth'],
#     prefix='/auth'
# )

# bcrypt_context = CryptContext(schemes=['bcrypt'],deprecrated='auto')

# secret_key = 'hahaha'
# algo = 'HS256'

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]
# oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

# def authenticate_user(username:str, password:str, db):
#     model = db.query(Users).filter(Users.user_name == username).first()
#     if not model:
#         return HTTPException(status_code=404, detail='User not found.')
#     if not bcrypt_context.verify(password, model.hashed_password):
#         return HTTPException(status_code=404, detail='Unauthenticated user.')
#     return model

# def generate_token(username:str, id:int, expires:timedelta):
#     encode = {'sub':username,'id':id}
#     expires = datetime.now(timezone.utc) + timedelta
#     encode.update({'expires':expires})
#     return jwt.encode(encode,secret_key,algorithm=[algo])

# def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
#     try:
#         payload = jwt.decode(token,secret_key,algorithms=[algo])
#         username = payload.get('sub')
#         id = payload.get('id')
#         if username is None or id is None:
#             return HTTPException(status_code=404, detail='User not found.')
#         return {'username':username, 'id':id}
#     except JWTError:
#         return HTTPException(status_code=404, detail='Token not generated')    

# @router.post('/token', status_code=status.HTTP_201_CREATED)
# def get_acccess_token(form:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
#     user = authenticate_user(form.username, form.password, db)
#     if not user:
#         return HTTPException(status_code=404, detail='User not found.')
#     token = generate_token(user.user_name, user.id, timedelta(minutes=20))
#     return {'access_token':token, 'token_type':'bearer'}