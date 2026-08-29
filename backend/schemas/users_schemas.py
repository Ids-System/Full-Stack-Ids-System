from pydantic import BaseModel,EmailStr

class Login(BaseModel):
    email : EmailStr
    password : str

class NewPassword(BaseModel):
    old_password : str
    new_password : str

class User_details(BaseModel):
    username : str
    email : str
    role : str

class AddUser(BaseModel):
    name : str
    email : EmailStr
    password : str

class UpdateRole(BaseModel):
    email : EmailStr
    role : str

class DeleteUser(BaseModel):
    email : EmailStr