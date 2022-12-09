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
    email: EmailStr
    password: str
    class Config:
        schema_extra = {
            "login_example" : {
                "email": "fikri@tes.com",
                "password": "password"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None