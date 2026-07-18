from sqlalchemy import Column,String,Integer
from db.database import SessionLocal,Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)


def add_user(name,password,email):
    with SessionLocal() as db:
        user = User(
            username = name,
            password = password,
            email = email
        )
        db.add(user)
        db.commit()


def get_user_byemail(email):
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        return user
    
