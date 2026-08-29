from fastapi import HTTPException,Request,WebSocket,WebSocketException,status
import jwt
from jwt import ExpiredSignatureError,InvalidTokenError
from datetime import datetime,UTC,timedelta
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def create_access_token(user_id,role):
    if SECRET_KEY is None:
        raise ValueError("Secret Key Not Configured")
    payload = {
        "userid" :user_id,
        "exp" : datetime.now(UTC)+timedelta(minutes=30),
        "type" : "access",
        "jti" : str(uuid.uuid4()),
        "role" : role
    }

    token = jwt.encode(payload,key=SECRET_KEY,algorithm=os.getenv("ALGORITHM"))

    return token


def create_refresh_token(user_id,role):
    if SECRET_KEY is None:
        raise ValueError("Secret Key Not Configured")
    payload = {
        "userid" :user_id,
        "exp" : datetime.now(UTC)+timedelta(days=30),
        "type" : "refresh",
        "jti" : str(uuid.uuid4()),
        "role" : role
    }

    token = jwt.encode(payload,key=SECRET_KEY,algorithm=os.getenv("ALGORITHM"))

    return token

def get_token_payload(request:Request,cookie_name:str = "access_token"):
    token = request.cookies.get(cookie_name)

    if token is None:
        raise HTTPException(
            401,detail="Authorization Token Missing"
        )

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
    

def get_refresh_payload(request:Request,cookie_name:str = "refresh_token"):
    token = request.cookies.get(cookie_name)

    if token is None:
        raise HTTPException(
            401,detail="Authorization Token Missing"
        )

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


def get_ws_payload(websocket:WebSocket):
    token = websocket.cookies.get("access_token")
    if token is None:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Unauthorized"
        )
    
    key = os.getenv("SECRET_KEY")
    if key is None:
        raise ValueError("Secret Key Not Configured")
    try:
        payload = jwt.decode(token, key=key, algorithms=[os.getenv("ALGORITHM")])
        return payload
    except ExpiredSignatureError:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Access token expired"
        )

    except InvalidTokenError:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Invalid access token"
        )
