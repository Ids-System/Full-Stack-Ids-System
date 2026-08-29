from db.database import Base,SessionLocal
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,func
from datetime import datetime

class Alerts(Base):
    __tablename__ = "alerts"
    alert_id = Column(Integer,autoincrement=True,primary_key=True)
    Attackid = Column(Integer,ForeignKey("attacks.attack_id",ondelete="CASCADE"))
    severity = Column(String,nullable = False)
    timestamp = Column(DateTime,default=func.now(),nullable=False)
    


def get_alerts():
    with SessionLocal() as db:
        alerts = db.query(Alerts).all()
        return alerts
    

def add_alerts(db,attackid,severity):
        alert = Alerts(
            Attackid = attackid,
            severity = severity,
        )
        db.add(alert)
        db.flush()
        db.refresh(alert)
        return alert

def clear_alerts(db):
    db.query(Alerts).delete()
    db.flush()