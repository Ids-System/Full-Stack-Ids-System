from fastapi import HTTPException
from models.Users_models import get_user_by_details,update_password
from auth.jwt_token import create_token
import bcrypt

def login_service(data):
    email,password = data.email,data.password
    is_auser = get_user_by_details(email)
    if is_auser:
        stored_password = is_auser.password
        is_valid = bcrypt.checkpw(password.encode("utf-8"),stored_password.encode("utf-8"))
        if is_valid:
            user_id = is_auser.id
            token = create_token(user_id)
            return token
        else:
            raise HTTPException(401,detail="Wrong Credentials")
    else:
        raise HTTPException(401,detail="User Not Found")


def get_user_details(user_id):
    details = get_user_by_details(usrid = user_id)
    if details :
        return details
    else :
        raise HTTPException(500,detail="Internal Server Error")


def update_user_password(user_id,old_pass,new_pass):
    is_auser = get_user_by_details(usrid=user_id)
    if is_auser:
        old_password = is_auser.password
        is_valid = bcrypt.checkpw(old_password,old_pass.encode("utf-8"))
        if is_valid:
            res = update_password(user_id,new_pass)
            if res : 
                return {"message" : "new password updated successfully"}
            else:
                raise HTTPException(500,detail="Internal Server Errror")
        else:
            raise HTTPException(401,detail="Invalid Credentials")
    else:
        raise HTTPException(401,detail="No User Found ")    