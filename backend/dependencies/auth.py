from fastapi import Depends
from auth.jwt_token import get_token_payload


def get_current_user(data= Depends(get_token_payload)):
    user_id = data["userid"]
    if user_id:
        return user_id
    else:
        return None


