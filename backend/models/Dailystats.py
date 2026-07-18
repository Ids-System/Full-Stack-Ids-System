from db.database import Base,SessionLocal
from sqlalchemy import Column,String,Integer,Date
from datetime import date

class Attack_Days(Base):
    __tablename__ = "attackdays"
    id = Column(Integer,primary_key=True,autoincrement=True)
    Date = Column(Date,default=date.today,nullable=False)
    no_of_attacks = Column(String,nullable=False)
    

def add_attacks(totalattack):
    with SessionLocal() as db:
        attacksday = Attack_Days(
            no_of_attacks = totalattack
        )
        db.add(attacksday)
        db.commit()

def remove_all_columns():
    with SessionLocal() as db:
        db.query(Attack_Days).delete()
        db.commit()

def get_attacksdays():
    with SessionLocal() as db:
        attacks = db.query(Attack_Days).all()
        return attacks

def get_attacksbydate(date):
    with SessionLocal() as db:
        attacks =  db.query(Attack_Days).filter(Attack_Days.Date == Date).first()
        if attacks:
            return attacks
            