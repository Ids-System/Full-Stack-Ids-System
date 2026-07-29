from fastapi import HTTPException
from models.Users_models import get_users,get_user_by_details,add_user,update_role,delete_user


def get_all_users(is_admin):
    if is_admin is None :
        raise HTTPException(403,detail="Forbidden")
    users = get_users()
    return {"users" : users}



def add_new_user(is_admin,data):
    if  is_admin is None :
        raise HTTPException(403,detail="Forbidden")
    email = data.email
    is_exists = get_user_by_details(email)
    if is_exists:
        raise HTTPException(409,detail="User Already Exists")
    name,email,password = data.name,data.email,data.password
    res = add_user(name,email,password)
    if res is None:
        raise HTTPException(500,detail="Internal Server Error")
    return {"message" : f" User '{name}' added sucessfully !"}


def update_user_role(is_admin,data):
    if is_admin is None:
        raise HTTPException(403,detail="Forbidden")
    email = data.email
    is_user = get_user_by_details(email)
    if is_user is None:
        raise HTTPException(404,detail="User Not Found")
    role = data.role
    res = update_role(email,role)
    if res is None:
        raise HTTPException(500,detail="Internal Server Error")
    return {"message" : "update successfully"}
    

def removeuser(is_admin,data):
    if is_admin is None:
            raise HTTPException(403,detail="Forbidden")
    email = data.email
    is_exists = get_user_by_details(email)
    if is_exists is None:
        raise HTTPException(404,detail="User Not Found")
    res = delete_user(email)
    if res is None:
        raise HTTPException(500,detail="Internal Server Error")
    return {"message" : "user deleted successfully"}