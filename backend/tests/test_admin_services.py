from services.admin_services import add_new_user,update_user_role,get_all_users,removeuser,table_cleanups
from unittest.mock import patch
from fastapi import HTTPException
import pytest

#Fetching Users

def test_get_all_users():
    users =[
        {
            "role": "admin",
            "id": 1,
            "username": "furkhan",
            "email": "mohdfurkhan9977@gmail.com",
            "password": "$2b$12$JQhqOcyYL0tPnFmyPSL60.8GAZW4VxqAqSSP5RWFJFME.9WD.N6bW"
        }
    ]
    with patch("services.admin_services.get_users") as mock_get_users:
        mock_get_users.return_value = users

        result = get_all_users(True)

        assert result == {"users":users}


def test_get_all_users_forbidden():
    with pytest.raises(HTTPException) as exc:
        get_all_users(None)
        assert exc.value.status_code == 403
        assert exc.value.detail == "Forbidden"

#Add Users

class NewUser():
     name = "Furkhan"
     email = "mohdfurkhan@gmail.com"
     password = "87964321"


def test_add_new_users():
    with patch("services.admin_services.get_user_by_details") as mock_get_user_details,\
         patch("services.admin_services.bcrypt.hashpw") as mock_hash_pw ,\
         patch("services.admin_services.add_user") as mock_add_user :
         mock_get_user_details.return_value = False
         mock_hash_pw.return_value =  b"$2b$12$JQhqOcyYL0tPnFmyPSL60.8GAZW4VxqAqSSP5RWFJFME.9WD.N6bW"
         mock_add_user.return_value = True

         result = add_new_user(True,data=NewUser)

         assert result == {"message" : " User 'Furkhan' added sucessfully !"}

def test_add_new_users_existing_user():
    with patch("services.admin_services.get_user_by_details") as mock_get_user_details:
         mock_get_user_details.return_value = True

         with pytest.raises(HTTPException) as exc:
            add_new_user(True,data=NewUser)
         assert exc.value.status_code == 409
         assert exc.value.detail == "User Already Exists"


def test_add_new_users_internal_server_error():
    with patch("services.admin_services.get_user_by_details") as mock_get_user_details,\
         patch("services.admin_services.bcrypt.hashpw") as mock_hash_pw ,\
         patch("services.admin_services.add_user") as mock_add_user :
         mock_get_user_details.return_value = False
         mock_hash_pw.return_value = b"$2b$12$JQhqOcyYL0tPnFmyPSL60.8GAZW4VxqAqSSP5RWFJFME.9WD.N6bW"
         mock_add_user.return_value = None

         with pytest.raises(HTTPException) as exc:
            add_new_user(True,data=NewUser)
         assert exc.value.status_code == 500
         assert exc.value.detail == "Internal Server Error"

def test_add_new_users_forbidden():
    with pytest.raises(HTTPException) as exc:
        add_new_user(None,data=NewUser)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Forbidden"

#Update Users

class GetUser():
    email = "mohdfurkhan@gmail.com"
    role = "admin"

def test_update_user_role():
    with patch("services.admin_services.get_user_by_details") as mock_get_details , \
         patch("services.admin_services.update_role") as  mock_update_role :
         mock_get_details.return_value = True
         mock_update_role.return_value = True

         result = update_user_role(True,data=GetUser)

         assert result == {"message" : "update successfully"}

def test_update_user_role_non_existing():
    with patch("services.admin_services.get_user_by_details") as mock_get_details:
        mock_get_details.return_value = None

        with pytest.raises(HTTPException) as exc:
            update_user_role(True,data=GetUser)

        assert exc.value.status_code == 404
        assert exc.value.detail == "User Not Found"


def test_update_user_role_Internal_error():
    with patch("services.admin_services.get_user_by_details") as mock_get_details , \
         patch("services.admin_services.update_role") as  mock_update_role :
         mock_get_details.return_value = True
         mock_update_role.return_value = None

         with pytest.raises(HTTPException) as exc:
             update_user_role(True,data=GetUser)
         assert exc.value.status_code == 500
         assert exc.value.detail == "Internal Server Error"


def test_update_user_role_forbidden():
    with pytest.raises(HTTPException) as exc:
        update_user_role(None,data=GetUser)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Forbidden"


#Remove Users

class DeleteUser():
    email = "mohd@gmail.com"

def test_remove_users():
    with patch("services.admin_services.get_user_by_details") as mock_get_details , \
         patch("services.admin_services.delete_user") as mock_delete_user:
         mock_get_details.return_value = True
         mock_delete_user.return_value = True

         result = removeuser(True,data=DeleteUser)

         assert result == {"message" : "user deleted successfully"}

def test_remove_user_non_existing():
    with patch("services.admin_services.get_user_by_details") as mock_get_details:
         mock_get_details.return_value = None
         with pytest.raises(HTTPException) as exc:
             removeuser(True,data=DeleteUser)
         assert exc.value.status_code == 404
         assert exc.value.detail == "User Not Found"

def test_remove_users_internal_erro():
    with patch("services.admin_services.get_user_by_details") as mock_get_details , \
         patch("services.admin_services.delete_user") as mock_delete_user:
         mock_get_details.return_value = True
         mock_delete_user.return_value = None

         with pytest.raises(HTTPException) as exc:
             removeuser(True,data=DeleteUser)
         assert exc.value.status_code == 500
         assert exc.value.detail == "Internal Server Error"

def test_remove_users_forbidden():
    with pytest.raises(HTTPException) as exc:
        removeuser(None,data=DeleteUser)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Forbidden"


#Module Clean Up Test
def test_table_cleanups_success():

    with patch("services.admin_services.SessionLocal") as mock_session, \
         patch("services.admin_services.clear_attackips") as mock_attackips, \
         patch("services.admin_services.clear_attacks") as mock_attacks, \
         patch("services.admin_services.clear_alerts") as mock_alerts, \
         patch("services.admin_services.clear_blockedip") as mock_blockedip, \
         patch("services.admin_services.clear_attack_days") as mock_attack_days:
        mock_db = mock_session.return_value.__enter__.return_value
        result = table_cleanups(True)
        assert result == {"message": "Clean Up Successfull"}
        mock_attackips.assert_called_once_with(mock_db)
        mock_attacks.assert_called_once_with(mock_db)
        mock_alerts.assert_called_once_with(mock_db)
        mock_blockedip.assert_called_once_with(mock_db)
        mock_attack_days.assert_called_once_with(mock_db)
        mock_db.commit.assert_called_once()
        mock_db.rollback.assert_not_called()

def test_table_cleanups_internal_error():

    with patch("services.admin_services.SessionLocal") as mock_session, \
         patch("services.admin_services.clear_attackips") as mock_attackips, \
         patch("services.admin_services.clear_attacks"), \
         patch("services.admin_services.clear_alerts"), \
         patch("services.admin_services.clear_blockedip"), \
         patch("services.admin_services.clear_attack_days"):
        mock_db = mock_session.return_value.__enter__.return_value
        mock_attackips.side_effect = Exception("Database error")
        with pytest.raises(HTTPException) as exc:
            table_cleanups(True)
        assert exc.value.status_code == 500
        assert exc.value.detail == "Database error"
        mock_db.rollback.assert_called_once()
        mock_db.commit.assert_not_called()


def test_table_cleanups_forbidden():
    with pytest.raises(HTTPException) as exc:
        table_cleanups(False)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Forbidden"