from fastapi import Depends
from auth.jwt_token import decode_token


def get_current_user(data= Depends(decode_token)):
    user_id = data["userid"]
    if user_id:
        return user_id
    else:
        return None


