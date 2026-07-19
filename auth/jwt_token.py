from fastapi import HTTPException,Header
import jwt
from jwt import ExpiredSignatureError,InvalidTokenError
from datetime import datetime,UTC,timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def create_token(user_id):
    key = os.getenv("SECRET_KEY")
    if key is None:
        raise ValueError("Secret Key Not Configured")
    payload = {
        "userid" :user_id,
        "exp" : datetime.now(UTC)+timedelta(minutes=30)
    }

    token = jwt.encode(payload,key=key,algorithm=os.getenv("ALGORITHM"))

    return token


def verify_token(authorization : str = Header(None)):
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
    
    