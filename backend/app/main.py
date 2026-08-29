from fastapi import FastAPI
from routes.users_routes import users
from routes.engine import engine
from routes.admin import admin
from routes.dashboard import dashboard
from routes.websockets import ws

app = FastAPI()
app.include_router(users)
app.include_router(engine)
app.include_router(admin)
app.include_router(dashboard)
app.include_router(ws)

def get_app():
    return app