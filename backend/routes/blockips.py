from fastapi import APIRouter

blockips = APIRouter(prefix="/blocked-ips")

@blockips.get('/')
def get_blockips():
    return {"message" : "all blocked ips"}

@blockips.post('/')
def add_api():
    return {"message" : "ip added in the blocked list"}

@blockips.delete('/{id}')
def remove_ip():
    return {"message" : "ip removed from block list"}
