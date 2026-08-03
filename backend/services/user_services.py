from fastapi import HTTPException
from datetime import datetime, UTC
from models.Users_models import get_user_by_details,update_password
from models.token_models import add_token,get_token
from auth.jwt_token import create_access_token,create_refresh_token,get_token_payload
import bcrypt

def login_service(data):
    email,password = data.email,data.password
    is_auser = get_user_by_details(email)
    if is_auser:
        stored_password = is_auser.password
        is_valid = bcrypt.checkpw(password.encode("utf-8"),stored_password.encode("utf-8"))
        if is_valid:
            user_id = is_auser.id
            role = is_auser.role
            access_token = create_access_token(user_id,role)
            refresh_token = create_refresh_token(user_id,role)
            return {"access_token" : access_token,"refresh_token":refresh_token}
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


def update_user_password(user_id,data):
    old_pass,new_pass = data.old_password,data.new_password
    is_auser = get_user_by_details(usrid=user_id)
    if is_auser:
        old_password = is_auser.password
        is_valid = bcrypt.checkpw(old_pass.encode("utf-8"),old_password.encode("utf-8"))
        if is_valid:
            hash_password = bcrypt.hashpw(new_pass,bcrypt.gensalt())
            res = update_password(user_id,hash_password)
            if res : 
                return {"message" : "new password updated successfully"}
            else:
                raise HTTPException(500,detail="Internal Server Errror")
        else:
            raise HTTPException(401,detail="Invalid Credentials")
    else:
        raise HTTPException(404,detail="No User Found")    


def refresh_token(payload):
    if payload["type"] != "refresh":
            raise HTTPException(401,detail="Invalid Token Type")
    jti = payload.get("jti")
    is_blacklisted = get_token(jti)
    if is_blacklisted :
        raise HTTPException(401,detail="Token has been revoked")
    role = payload.get("role")
    new_token = create_access_token(payload.get("userid"),role)
    return {"access_token" : new_token}


def user_logout(token):
    jti = token.get("jti")
    exp = token.get("exp")
    res = add_token(jti,exp)
    if res:
        return {"message" : "user logout successfully"}
    else:
        raise HTTPException(500,detail="Internal Server Error")