from fastapi import FastAPI
from routes.users_routes import users

app = FastAPI()
app.include_router(users)

def get_app():
    return app