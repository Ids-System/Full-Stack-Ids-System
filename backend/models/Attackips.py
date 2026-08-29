from sqlalchemy import Column,String,Integer,DateTime,func
from sqlalchemy.dialects.postgresql import INET
from db.database import SessionLocal,Base


class AttackIP(Base):
    __tablename__ = "ips"
    ip_id = Column(Integer,autoincrement=True,primary_key=True)
    source_ip = Column(INET,nullable=False)
    destination_ip = Column(INET,nullable=False)
    protocol = Column(String(10),nullable=False)
    port = Column(Integer,nullable=False)
    timestamp = Column(DateTime,default=func.now(),nullable=False)


def get_ips():
    with SessionLocal() as db:
       packets = db.query(AttackIP).all()
       return packets 

def add_ips(db,sip,dip,protocol,port):
        ip = AttackIP(
            source_ip = sip,
            destination_ip = dip,
            protocol = protocol,
            port = port
        )
        db.add(ip)
        db.flush()
        db.refresh(ip)
        return ip


def clear_attackips(db):
    db.query(AttackIP).delete()
    db.flush()