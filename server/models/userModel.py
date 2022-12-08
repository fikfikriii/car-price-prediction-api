from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    class Config:
        schema_extra = {
            "user_example" : {
                "name": "fikri",
                "email": "fikri@tes.com",
                "password": "password"
            }
        }

class Login(BaseModel):
    username: str
    password: str
    class Config:
        schema_extra = {
            "login_example" : {
                "username": "fikri",
                "password": "password"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None