from db.database import Base,SessionLocal
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,func
from datetime import datetime

class Alerts(Base):
    __tablename__ = "alerts"
    alert_id = Column(Integer,autoincrement=True,primary_key=True)
    Attackid = Column(Integer,ForeignKey("attacks.attack_id"))
    severnity = Column(String,nullable = False)
    timestamp = Column(DateTime,default=func.now(),nullable=False)
    status = Column(String,nullable=False)


def get_alerts():
    with SessionLocal() as db:
        alerts = db.query(Alerts).all()
        return alerts
    

def add_alerts(attackid,severnity,status):
    with SessionLocal() as db:
        alert = Alerts(
            Attackid = attackid,
            severnity = severnity,
            status = status
        )
        db.add(alert)
        db.commit()

def delete_alerts(alert_id):
    with SessionLocal() as db:
        alerts = db.query(Alerts.alert_id == alert_id).first()
        if alerts:
            db.delete(alerts)
            db.commit()

