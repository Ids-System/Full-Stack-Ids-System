from fastapi import APIRouter

engine = APIRouter(prefix="/engine")

@engine.post('/report')
def report():
    return {"message" : "report processed"}