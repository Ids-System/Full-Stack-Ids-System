from fastapi import APIRouter
from services.user_services import login_service
from schemas.users_schemas import Login
users = APIRouter(prefix="/users")

@users.post('/login')
def login(data : Login):
    return login_service(data)

@users.get('/me')
def users_details():
    return "users"

@users.put('/password')
def change_password():
    return "Change Password"


