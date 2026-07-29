from fastapi import HTTPException,Header
import jwt
from jwt import ExpiredSignatureError,InvalidTokenError
from datetime import datetime,UTC,timedelta
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def create_access_token(user_id):
    if SECRET_KEY is None:
        raise ValueError("Secret Key Not Configured")
    payload = {
        "userid" :user_id,
        "exp" : datetime.now(UTC)+timedelta(minutes=30),
        "type" : "access",
        "jti" : str(uuid.uuid4())
    }

    token = jwt.encode(payload,key=SECRET_KEY,algorithm=os.getenv("ALGORITHM"))

    return token


def create_refresh_token(user_id):
    if SECRET_KEY is None:
        raise ValueError("Secret Key Not Configured")
    payload = {
        "userid" :user_id,
        "exp" : datetime.now(UTC)+timedelta(days=30),
        "type" : "refresh",
        "jti" : str(uuid.uuid4())
    }

    token = jwt.encode(payload,key=SECRET_KEY,algorithm=os.getenv("ALGORITHM"))

    return token

def get_token_payload(authorization : str = Header(None)):
    if authorization is None:
        raise HTTPException(
            401,detail="Authorization Token Missing"
        )
    token = authorization.replace("Bearer ", "")

    key = os.getenv("SECRET_KEY")
    if key is None:
        raise ValueError("Secret Key Not Configured")
    try:
        payload = jwt.decode(token,key=key,algorithms=[os.getenv("ALGORITHM")])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(401,detail="Token Expired")
    except InvalidTokenError:
        raise HTTPException(401,detail="Invalid Token")
    
    