from db.database import Base,SessionLocal
from sqlalchemy import Column,String,Integer,Date
from datetime import date

class AttackDays(Base):
    __tablename__ = "attackdays"
    id = Column(Integer,primary_key=True,autoincrement=True)
    date = Column(Date,default=date.today,nullable=False)
    no_of_attacks = Column(Integer,nullable=False)


def get_attack_date(db,date):
    res = db.query(AttackDays).filter(AttackDays.date == date).first()
    return res

def add_no_attacks(db,count):
        attacksday = AttackDays()
        attacksday.no_of_attacks = count
        db.add(attacksday)
        db.flush()
        db.refresh(attacksday)

def increment_count(db,date):
    attack = db.query(AttackDays).filter(AttackDays.date == date).first()
    attack.no_of_attacks +=1
    db.flush()

def clear_attack_days(db):
    db.query(AttackDays).delete()
    db.flush()

def get_attacksdays():
    with SessionLocal() as db:
        attacks = db.query(AttackDays).all()
        return attacks





            