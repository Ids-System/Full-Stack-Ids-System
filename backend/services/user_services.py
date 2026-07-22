from fastapi import HTTPException
from datetime import datetime, UTC
from models.Users_models import get_user_by_details,update_password
from models.token_models import add_token,get_token
from auth.jwt_token import create_access_token,create_refresh_token,decode_token
import bcrypt

def login_service(data):
    email,password = data.email,data.password
    is_auser = get_user_by_details(email)
    if is_auser:
        stored_password = is_auser.password
        is_valid = bcrypt.checkpw(password.encode("utf-8"),stored_password.encode("utf-8"))
        if is_valid:
            user_id = is_auser.id
            access_token = create_access_token(user_id)
            refresh_token = create_refresh_token(user_id)
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
        raise HTTPException(401,detail="No User Found ")    


def refresh_token(authorization):
    if authorization is None:
        raise HTTPException(
            401,detail="Authorization Token Missing"
        )
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    jti = payload.get("jti")
    not_valid_token = get_token(jti)
    if not_valid_token:
        raise HTTPException(401,detail="Token has been revoked")
    if payload["type"] != "refresh":
        raise HTTPException(401,detail="Invalid Token Type")
       
    new_token = create_access_token(payload.get("userid"))
    return {"access_token" : new_token}


def user_logout(token):
    jti = token.get("jti")
    exp = token.get("exp")
    res = add_token(jti,exp)
    if res:
        return {"message" : "user logout successfully"} 