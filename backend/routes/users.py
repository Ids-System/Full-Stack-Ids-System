from fastapi import APIRouter

users = APIRouter(prefix="/users")

@users.post('/login')
def login():
    return "users login"

@users.get('/me')
def users_details():
    return "users"

@users.put('/password')
def change_password():
    return "Change Password"


