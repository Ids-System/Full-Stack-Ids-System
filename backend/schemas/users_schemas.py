from pydantic import BaseModel,EmailStr

class Login(BaseModel):
    email : EmailStr
    password : str

class NewPassword(BaseModel):
    old_password : str
    new_password : str

