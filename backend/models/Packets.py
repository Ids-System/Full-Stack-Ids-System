from sqlalchemy import Column,String,Integer
from db.database import SessionLocal,Base

class Packets(Base):
    __tablename__ = "packets"
    id = Column(Integer,autoincrement=True,primary_key=True)
    source_ip = Column(String,nullable=False)
    destination_ip = Column(String,nullable=False)
    protocol = Column(String,nullable=False)
    packet_size = Column(String,nullable=False)
    timestamp = Column(String,nullable=False)


def get_packets():
    with SessionLocal() as db:
       packets = db.query(Packets).all()
       return packets 