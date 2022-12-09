from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Request,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from server.auth.hash_password import Hash
from server.auth.jwt_handler import create_access_token
from server.auth.authenticate import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from server.models.userModel import User
from fastapi import APIRouter
from server.config.database import users_collection

user_router = APIRouter(
	tags = ['User']
)

def user_serializer(user) -> dict:
    return{
        "name": user["name"],
        "email": user["email"]
    }

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]

@user_router.post('/register')
def create_user(request:User) -> dict:
	hashed_pass = Hash.bcrypt(request.password)
	user_object = dict(request)
	user_object["password"] = hashed_pass
	if users_collection.find_one({"email": request.email}):
		return {"Message": "Email already exist"}
	users_collection.insert_one(user_object)
	return {"User successfully created"}

@user_router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
	user = users_collection.find_one({"email":request.username})
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} email')
	if not Hash.verify(user["password"],request.password):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
	access_token = create_access_token(data={"sub": user["email"] })
	return {"access_token": access_token, "token_type": "bearer"}

@user_router.get('/show_user')
def show_user():
    list_user = []
    for user in users_serializer(users_collection.find()):
        list_user.append(user)
    return list_user