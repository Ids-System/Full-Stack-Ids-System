from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from dependencies.auth import is_admin
from services.admin_services  import get_all_users,add_new_user,update_user_role,removeuser
from services.admin_services import table_cleanups
from schemas.users_schemas import AddUser,UpdateRole,DeleteUser
from services.report_services import generate_pdf_report


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
def delete_ips(isadmin = Depends(is_admin)):
    return table_cleanups(isadmin) # Fixed the typo/bug passing the function is_admin instead of local variable isadmin


@admin.get('/export')
def export_report(isadmin = Depends(is_admin)):
    if isadmin is None:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        pdf_buffer = generate_pdf_report()
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=ids_security_report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

