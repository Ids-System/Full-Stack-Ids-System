from fastapi import APIRouter,Depends
from services.engine_services import proces_report
from schemas.engine_report_schema import Report
from auth.engine_auth import verify_engine
engine = APIRouter(prefix="/engine")

@engine.post('/report')
async def report(data:Report,is_verified = Depends(verify_engine)):
    return await proces_report(is_verified,data)


