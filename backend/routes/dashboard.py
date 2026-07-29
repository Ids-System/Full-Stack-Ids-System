from fastapi import APIRouter

dashboard = APIRouter(prefix="/dashboard")

@dashboard.get('/statistics')
def get_noofattacks():
    return {"message" : "no of attacks"}

@dashboard.get('/attacks')
def get_attacks():
    return {"message" : "all attacks"}

@dashboard.get('/attack-ips')
def get_ips():
    return {"message" : "attack ips"}

@dashboard.get('/block-ips')
def get_blockips():
    return {"message" : "all blocked ips"}