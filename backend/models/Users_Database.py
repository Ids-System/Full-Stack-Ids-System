from sqlalchemy import Column,String,Integer
from db.database import SessionLocal,Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    role = Column(String,nullable=False)


def add_user(name,password,role):
    with SessionLocal() as db:
        user = User(
            username = name,
            password = password,
            role = role
        )
        db.add(user)
        db.commit()


def get_user_byname(name):
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == name).first()
        return user
    
