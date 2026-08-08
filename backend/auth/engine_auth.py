import os 
import secrets
from dotenv import load_dotenv
from fastapi import HTTPException,Security
from fastapi.security import APIKeyHeader

load_dotenv()

engine_api_key = APIKeyHeader(
    name="X-Engine-Key",
    auto_error=False
)

def verify_engine(api_key : str | None = Security(engine_api_key)):
    expect_key = os.getenv("ENGINE_KEY")
    if expect_key is None:
        raise RuntimeError("Engine_key Not Configured")
    if api_key is None:
        raise HTTPException(401,detail= "Api Key Missing")
    if not secrets.compare_digest(api_key,expect_key):
        raise HTTPException(403,detail="Invalid Api Key")
    return True