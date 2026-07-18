from sqlalchemy import Column,String,Integer,Date
from db.database import Base,SessionLocal
from sqlalchemy.dialects.postgresql import INET
from datetime import date

class Blockedips(Base):
    __tablename__ = "blockedips"
    ip_id = Column(Integer,autoincrement=True,primary_key=True)
    ip = Column(INET,nullable=False)
    Attack = Column(String,nullable=False)
    Date_of_block = Column(Date,default=date.today,nullable=False)


def get_blocked_ips():
    with SessionLocal() as db:
        bips = db.query(Blockedips).all()
        return bips
    

def add_blockip(ip,attack):
    with SessionLocal() as db:
        ip = Blockedips(
            ip = ip,
            Attack = attack
        )
        db.add(ip)
        db.commit()


def remove_ip(ipid):
    with SessionLocal() as db:
        ip = db.query(Blockedips).filter(Blockedips.ip_id == ipid).first()
        if ip:
            db.delete(ip)
            
