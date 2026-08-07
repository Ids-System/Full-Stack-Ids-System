from fastapi import APIRouter,Depends,Response
from services.user_services import login_service,get_user_details,update_user_password,refresh_token,user_logout
from dependencies.auth import get_current_user
from auth.jwt_token import get_token_payload,get_refresh_payload
from schemas.users_schemas import Login,NewPassword
users = APIRouter(prefix="/users")

@users.post('/login')
def login(data : Login,response:Response):
    access_token,refresh_token = login_service(data)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax"
        )
    return {
        "message": "Login Successful"
    }

@users.get('/me')
def users_details(user_id = Depends(get_current_user)):
    return get_user_details(user_id)

@users.put('/password')
def change_password(data:NewPassword,user_id = Depends(get_current_user)):
    return update_user_password(user_id,data)


@users.post('/refresh')
def refreshtoken(response:Response,payload = Depends(get_refresh_payload)):
    access_token = refresh_token(payload)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {
        "message": "Access token refreshed"
    }


@users.post('/logout')
def logout(response:Response,paylaod = Depends(get_refresh_payload)):
    token = paylaod
    result = user_logout(token)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return result