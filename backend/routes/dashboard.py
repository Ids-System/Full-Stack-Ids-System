from fastapi import APIRouter,Depends
from dependencies.auth import get_current_user
from services.dashboard_services import fetch_alerts,fetch_attacks,fetch_blocked_ips,fetch_ips,fetch_statistics


dashboard = APIRouter(prefix="/dashboard")

@dashboard.get('/attack-ips')
def get_ips(is_user = Depends(get_current_user)):
    return fetch_ips(is_user)

@dashboard.get('/attacks')
def get_attacks(is_user = Depends(get_current_user)):
    return fetch_attacks(is_user)

@dashboard.get('/alerts')
def get_alerts(is_user = Depends(get_current_user)):
    return fetch_alerts(is_user)

@dashboard.get('/block-ips')
def get_blockips(is_user = Depends(get_current_user)):
    return fetch_blocked_ips(is_user)

@dashboard.get('/statistics')
def get_noofattacks(is_user = Depends(get_current_user)):
    return fetch_statistics(is_user)
