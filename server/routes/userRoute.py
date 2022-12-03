from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Request,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from auth.hash_password import Hash
from auth.jwt_handler import create_access_token
from auth.authenticate import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from models.userModel import User
from fastapi import APIRouter
from config.database import users_collection

user_router = APIRouter()

@user_router.get("/", tags=["Root"])
def read_root(current_user:User = Depends(get_current_user)):
	return {"data":"Ini udh terautentikasi"}

@user_router.get("/home", tags=["Root"])
def print_home(current_user:User = Depends(get_current_user)):
	return ("Selamat Datang!")

@user_router.post('/register', tags=["User"])
def create_user(request:User):
	hashed_pass = Hash.bcrypt(request.password)
	user_object = dict(request)
	user_object["password"] = hashed_pass
	if users_collection.find_one({"username": request.username}):
		return {"Message": "Username already exist"}
	user_id = users_collection.insert_one(user_object)
	# print(user)
	return {"User":"created"}

@user_router.post('/login', tags=["User"])
def login(request:OAuth2PasswordRequestForm = Depends()):
	user = users_collection.find_one({"username":request.username})
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
	if not Hash.verify(user["password"],request.password):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
	access_token = create_access_token(data={"sub": user["username"] })
	return {"access_token": access_token, "token_type": "bearer"}