from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr = None

class UserLogin(BaseModel):
    username: str
    password: str

