from db.database import Base,SessionLocal
from sqlalchemy import Column,String,Integer,ForeignKey,func,select,Date


class Attacks(Base):
    __tablename__ = "attacks"
    attack_id = Column(Integer,autoincrement=True,primary_key=True)
    ip_id = Column(Integer,ForeignKey("ips.ip_id"),nullable=False)
    attack = Column(String,nullable=False)
    description = Column(String,nullable=False)
    date = Column(Date, default=func.now(), nullable=False)


def get_attacks():
    with SessionLocal() as db:
        return db.query(Attacks).all()


def count_attacks(db,date):
          count = db.scalar(
            select(func.count()).select_from(Attacks.date == date)
                            )
          return count


def add_attack(db,ip_id,attack,description):
        attack = Attacks(
            ip_id = ip_id,
            attack = attack,
            description = description
        )
        db.add(attack)
        db.flush()
        db.refresh(attack)
        return attack

def delete_attacks(attack_id):
    with SessionLocal() as db:
        aip = db.query(Attacks.attack_id == attack_id).first()
        db.delete(aip)
        db.commit(aip)
        