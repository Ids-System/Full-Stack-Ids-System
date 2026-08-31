from sqlalchemy import Column,String,Integer
from db.database import SessionLocal,Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    role = Column(String(20),nullable=False,default="observer")

def get_users():
    with SessionLocal() as db:
        users = db.query(User).all()
        return users


def get_user_by_details(email = None,usrid = None):
    with SessionLocal() as db:
        if email is not None:
            user = db.query(User).filter(User.email == email).first()
        elif id is not None:
            user = db.query(User).filter(User.id == usrid).first()
        return user

def add_user(name,password,email):
    with SessionLocal() as db:
        user = User(
            username = name,
            password = password,
            email = email
        )
        db.add(user)
        db.commit()
        return True


def update_password(usrid,new_password):
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == usrid).first()
        if user:
            user.password = new_password
            db.commit()
            return new_password
    

def update_role(email,new_role):
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        user.role = new_role
        db.commit()
        return True

def delete_user(email):
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.delete(user)
            db.commit()
            return True
            
