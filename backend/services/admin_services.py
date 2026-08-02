from fastapi import HTTPException
from db.database import SessionLocal
from models.Users_models import get_users,get_user_by_details,add_user,update_role,delete_user
from models.Attacks import clear_attacks
from models.Alerts import clear_alerts
from models.Attackips import clear_attackips
from models.Blocked_ips import clear_blockedip
from models.statistics import clear_attack_days
import bcrypt


def get_all_users(is_admin):
    if is_admin is None :
        raise HTTPException(403,detail="Forbidden")
    users = get_users()
    return {"users" : users}



def add_new_user(is_admin,data):
    if  is_admin is None :
        raise HTTPException(403,detail="Forbidden")
    email = data.email
    is_exists = get_user_by_details(email)
    if is_exists:
        raise HTTPException(409,detail="User Already Exists")
    name,email,password = data.name,data.email,data.password
    hash_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    res = add_user(name,email,hash_password)
    if res is None:
        raise HTTPException(500,detail="Internal Server Error")
    return {"message" : f" User '{name}' added sucessfully !"}


def update_user_role(is_admin,data):
    if is_admin is None:
        raise HTTPException(403,detail="Forbidden")
    email = data.email
    is_user = get_user_by_details(email)
    if is_user is None:
        raise HTTPException(404,detail="User Not Found")
    role = data.role
    res = update_role(email,role)
    if res is None:
        raise HTTPException(500,detail="Internal Server Error")
    return {"message" : "update successfully"}
    

def removeuser(is_admin,data):
    if is_admin is None:
            raise HTTPException(403,detail="Forbidden")
    email = data.email
    is_exists = get_user_by_details(email)
    if is_exists is None:
        raise HTTPException(404,detail="User Not Found")
    res = delete_user(email)
    if res is None:
        raise HTTPException(500,detail="Internal Server Error")
    return {"message" : "user deleted successfully"}


def table_cleanups(is_admin):
    if not is_admin :
        raise HTTPException(403,detail="Forbidden")
    with SessionLocal() as db:
        try :
                clear_attackips(db)
                clear_attacks(db)
                clear_alerts(db)
                clear_blockedip(db)
                clear_attack_days(db)
                db.commit()
                return {"message":"Clean Up Successfull"}
        except Exception as e:
            db.rollback()
            raise HTTPException(500,detail=str(e))
        

