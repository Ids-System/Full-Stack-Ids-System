from fastapi import APIRouter,Depends,Header
from services.user_services import login_service,get_user_details,update_user_password,refresh_token,user_logout
from dependencies.auth import get_current_user
from auth.jwt_token import get_token_payload
from schemas.users_schemas import Login,NewPassword
users = APIRouter(prefix="/users")

@users.post('/login')
def login(data : Login):
    return login_service(data)

@users.get('/me')
def users_details(user_id = Depends(get_current_user)):
    return get_user_details(user_id)

@users.put('/password')
def change_password(data:NewPassword,user_id = Depends(get_current_user)):
    return update_user_password(user_id,data)


@users.post('/refresh')
def refreshtoken(payload = Depends(get_token_payload)):
    access_token = refresh_token(payload)
    return access_token


@users.post('/logout')
def logout(paylaod = Depends(get_token_payload)):
    token = paylaod
    return user_logout(token)