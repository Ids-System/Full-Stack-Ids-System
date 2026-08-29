from fastapi import HTTPException
from models.Alerts import get_alerts
from models.Attackips import get_ips
from models.Attacks import get_attacks
from models.Blocked_ips import get_blocked_ips
from models.statistics import get_attacksdays

def fetch_ips(is_user):
    if not is_user:
        raise HTTPException(401,detail="Unauthorized Access")
    data = get_ips()
    return {"data" : data}

def fetch_attacks(is_user):
    if not is_user:
        raise HTTPException(401,detail="Unauthorized Access")
    data = get_attacks()
    return {"data" : data}

def fetch_alerts(is_user):
    if not is_user:
        raise HTTPException(401,detail="Unauthorized Access")
    data = get_alerts()
    return {"data" : data}

def fetch_statistics(is_user):
    if not is_user:
        raise HTTPException(401,detail="Unauthorized Access")
    data = get_attacksdays()
    return {"data" : data}

def fetch_blocked_ips(is_user):
    if not is_user:
        raise HTTPException(401,detail="Unauthorized Access")
    data = get_blocked_ips()
    return {"data" : data}

