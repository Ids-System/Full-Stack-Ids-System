from db.database import Base,SessionLocal
from datetime import datetime, UTC
from sqlalchemy import Column,VARCHAR,Integer,DateTime,func

class TokenBlacklist(Base):
    __tablename__ = "tokenblacklist"
    id = Column(Integer,autoincrement=True,primary_key=True)
    jti = Column(VARCHAR,unique=True,nullable=False)
    expires_at = Column(DateTime,nullable=False)
    blocked_at = Column(DateTime,default=func.now())

def get_token(jti):
    with SessionLocal() as db:
        token = db.query(TokenBlacklist).filter(TokenBlacklist.jti == jti).first()
        if token:
            return True
        else:
            return False


def add_token(jti,exp):
    with SessionLocal() as db:
        token  = TokenBlacklist(
            jti = jti,
            expires_at = datetime.fromtimestamp(exp, tz=UTC)
        )
        db.add(token)
        db.commit()
        return True


