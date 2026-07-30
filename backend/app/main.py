from fastapi import FastAPI
from routes.users_routes import users
from routes.engine import engine
from routes.admin import admin
from routes.dashboard import dashboard

app = FastAPI()
app.include_router(users)
app.include_router(engine)
app.include_router(admin)
app.include_router(dashboard)

def get_app():
    return app