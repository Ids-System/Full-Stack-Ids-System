from fastapi import APIRouter

dailyattacks = APIRouter(prefix="/daily-attacks")

@dailyattacks.get('/')
def get_noofattacks():
    return {"message" : "no of attacks"}


@dailyattacks.post('/')
def add_newattacks():
    return {"message" : "new attacks added"}

@dailyattacks.delete('/')
def deleteattacks():
    return {"message" : "attacks deleted"}