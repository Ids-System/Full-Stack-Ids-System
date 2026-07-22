from fastapi import Depends
from auth.jwt_token import verify_token


def user_id(data= Depends(verify_token)):
    user_id = data["userid"]
    if user_id:
        return user_id
    else:
        return None


