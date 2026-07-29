from fastapi import APIRouter,Depends
from dependencies.auth import is_admin
from services.admin_services  import get_all_users,add_new_user,update_user_role,removeuser
from schemas.users_schemas import AddUser,UpdateRole,DeleteUser

admin = APIRouter(prefix="/admin")

@admin.get('/users')
def getusers(isadmin = Depends(is_admin)):
    users = get_all_users(isadmin)
    return users

@admin.post('/users')
def addusers(data : AddUser,isadmin = Depends(is_admin)):
    res = add_new_user(isadmin,data)
    return res

@admin.patch('/users')
def updaterole(data :UpdateRole, isadmin = Depends(is_admin)):
    res = update_user_role(isadmin,data)
    return res

@admin.delete('/users')
def deleteuser(data :DeleteUser ,isadmin = Depends(is_admin)):
    res = removeuser(isadmin,data)
    return res

@admin.delete('/attack-history')
def delete_ips():
    return {"message" : "delete ips"}


@admin.delete('/block-ips/{id}')
def remove_ip():
    return {"message" : "ip removed from block list"}


@admin.get('/export')
def export_report():
    return {"message" : "export eraly report"}
