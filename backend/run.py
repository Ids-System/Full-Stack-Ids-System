from contextlib import asynccontextmanager
from fastapi import FastAPI
from models.Alerts import Alerts
from models.Attackips import AttackIP
from models.Attacks import Attacks
from models.statistics import AttackDays
from models.Blocked_ips import Blockedips
from models.Users_models import User
from models.token_models import TokenBlacklist
from app.main import get_app
from fastapi.middleware.cors import CORSMiddleware

from db.database import Base, engine


Base.metadata.create_all(bind=engine)

app = get_app()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)