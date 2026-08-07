from fastapi import APIRouter
from services.engine_services import proces_report
from schemas.engine_report_schema import Report
engine = APIRouter(prefix="/engine")

@engine.post('/report')
async def report(data:Report):
    return await proces_report(True,data)

