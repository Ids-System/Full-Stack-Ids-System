from fastapi import APIRouter

attack_ip = APIRouter(prefix="/attack-ips")

@attack_ip.get('/')
def get_ips():
    return {"message" : "attack ips"}

@attack_ip.post('/')
def add_ip():
    return {"message" : "add attack ip"}

@attack_ip.delete('/')
def delete_ips():
    return {"message" : "delete ips"}