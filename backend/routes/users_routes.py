from fastapi import APIRouter,Depends
from services.user_services import login_service,get_user_details,update_user_password
from dependencies.auth import user_id
from schemas.users_schemas import Login,NewPassword
users = APIRouter(prefix="/users")

@users.post('/login')
def login(data : Login):
    return login_service(data)

@users.get('/me')
def users_details(user_id = Depends(user_id)):
    return get_user_details(user_id)

@users.put('/password')
def change_password(data:NewPassword,user_id = Depends(user_id)):
    return update_user_password(user_id,data)


