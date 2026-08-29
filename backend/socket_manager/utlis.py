from models.Alerts import get_alerts
from models.Attackips import get_ips
from models.Attacks import get_attacks
from models.Blocked_ips import get_blocked_ips
from models.statistics import get_attacksdays
from fastapi.encoders import jsonable_encoder

async def live_report_genrator():
    ip = get_ips()
    attack = get_attacks()
    alerts = get_alerts()
    blocked_ip = get_blocked_ips()
    stats = get_attacksdays()

    return jsonable_encoder ({
        "event" : "report_processed",
        "data" : {
            "attack_ip" : ip,
            "attack" : attack,
            "alerts" : alerts,
            "blocked_ip" : blocked_ip,
            "statistics" : stats
        }
    })

