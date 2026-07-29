from fastapi import APIRouter

attacks = APIRouter(prefix="/attacks")

@attacks.get('/')
def get_attacks():
    return {"message" : "all attacks"}

@attacks.post('/')
def add_attacks():
    return {"message" : "attacks added"}

@attacks.delete('/')
def delete_attacks():
    return {"message" : "attacks deleted "}
