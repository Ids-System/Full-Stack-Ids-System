from fastapi import HTTPException
from datetime import date
from db.database import SessionLocal
from models.Attackips import add_ips
from models.Attacks import add_attack
from models.Alerts import add_alerts
from models.Blocked_ips import add_blockip
from models.statistics import add_no_attacks,get_attack_date,increment_count
from socket_manager.manager import manager
from socket_manager.utlis import live_report_genrator

async def proces_report(is_validate,data):
    if is_validate is None:
        raise HTTPException(401,detail="Unauthorized")
    with SessionLocal() as db:
        try:
            ip = add_ips(
                db,
                str(data.source_ip),
                str(data.destination_ip),
                data.protocol,
                data.port)
            attack = add_attack(
                db,
                ip.ip_id,
                data.attack,
                description=data.description
            )
            alert = add_alerts(
                db,
                attack.attack_id,
                data.severity
            )
            if data.severity == "High":
                blacklist_ip = add_blockip(
                    db,
                    str(data.source_ip),
                    data.attack
                )
            
            todays_date = date.today() 
            is_record_exists = get_attack_date(db,todays_date)
            if is_record_exists:
                increment_count(db,todays_date)
            else:
                add_no_attacks(db,1)
            db.commit()
            report = await live_report_genrator()
            await manager.broadcast_msg(report)
            return {"message" : "report processed sucessfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500,detail=str(e))
