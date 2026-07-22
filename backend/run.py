from contextlib import asynccontextmanager
from fastapi import FastAPI
from models.Alerts import Alerts
from models.Attackips import AttackIP
from models.Attacks import Attacks
from models.Attacksstats import Attack_Days
from models.Blocked_ips import Blockedips
from models.Users_models import User
from models.token_models import TokenBlacklist
from app.main import get_app

from db.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    yield

app = get_app()