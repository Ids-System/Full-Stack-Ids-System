import pytest
from unittest.mock import patch
from services.user_services import login_service,get_user_details,update_user_password,refresh_token,user_logout
from fastapi import HTTPException


#Login Service Tests

class LoginUser():
    def __init__(self):
        self.id = 1
        self.email = "aizen@gmail.com"
        self.password = "Mf#@9346954045"

class Data():
    def __init__(self):
        self.email = "aizen@gmail.com"
        self.password = "Mf#@9346954045"


def test_login():

    with patch("services.user_services.get_user_by_details") as mock_get_user, \
         patch("services.user_services.bcrypt.checkpw") as mock_check, \
         patch("services.user_services.create_access_token") as mock_access_token, \
         patch("services.user_services.create_refresh_token") as mock_refresh_token :

         mock_get_user.return_value = LoginUser()
         mock_check.return_value = True
         mock_access_token.return_value =  "fasdfasdfw3wqt546745udyjfjfg.63456346w.t6.56347.74"
         mock_refresh_token.return_value = "fasdfasdfw3wqt546745udyjfjfg.63456346w.t6.56347.74"

         result = login_service(Data())
         assert result == {
            "access_token": "fasdfasdfw3wqt546745udyjfjfg.63456346w.t6.56347.74",
            "refresh_token": "fasdfasdfw3wqt546745udyjfjfg.63456346w.t6.56347.74"
            }

def test_login_with_wrong_credentials():

    with patch("services.user_services.get_user_by_details") as mock_get_user, \
         patch("services.user_services.bcrypt.checkpw") as mock_check:
         mock_get_user.return_value = LoginUser()
         mock_check.return_value = False

         with pytest.raises(HTTPException):
            login_service(Data())

def test_login_with_user_not_found():
     with patch("services.user_services.get_user_by_details") as mock_get_user:
        mock_get_user.return_value = None
        with pytest.raises(HTTPException) as exc:
            login_service(Data())
        assert exc.value.status_code == 401
        assert exc.value.detail == "User Not Found"


#User Detail Fetch Service Tests

class UserDetails():
    def __init__(self):
        self.name = "Aizen"
        self.email = "aizen123@gmail.com"
        self.role = "observer"

def test_get_user_details():
    with patch("services.user_services.get_user_by_details") as mock_get_details:
        expected = UserDetails()
        mock_get_details.return_value = expected

        result = get_user_details(1)

        assert result is expected


def test_get_user_details_no_user_found():
    with patch("services.user_services.get_user_by_details") as mock_get_details:
        mock_get_details.return_value = None
        with pytest.raises(HTTPException):
            get_user_details(1)

#Password Update Tests
class Password():
    def __init__(self):
        self.old_password="Mf#@9346954045"
        self.new_password = "Mf#@00225588"


class User():
    def __init__(self):
        self.id = 1
        self.name = "Aizen"
        self.email = "aizen@gmail.com"
        self.password = "Mf#@9346954045"

def test_update_password():
        with    patch("services.user_services.get_user_by_details") as mock_getuser,\
                patch("services.user_services.bcrypt.checkpw") as mock_checkpw,\
                patch("services.user_services.bcrypt.hashpw") as mock_hashpw,\
                patch("services.user_services.update_password") as mock_updatepassword:

                mock_getuser.return_value = User()
                mock_checkpw.return_value = True
                mock_hashpw.return_value = "vlbblb62l3kb6lkqb2libu4629570b79by"
                mock_updatepassword.return_value = True

                result = update_user_password(1,data = Password())

                assert result == {"message" : "new password updated successfully"}

def test_upate_password_without_user():
    with patch("services.user_services.get_user_by_details") as mock_getuser:
        mock_getuser.return_value = None

        with pytest.raises(HTTPException) as exc:
            update_user_password(1,Password())
            assert exc.value.status_code == 404
            assert exc.value.detail == "No User Found"


def test_update_password_with_wrong_credentials():
    with    patch("services.user_services.get_user_by_details") as mock_getuser, \
            patch("services.user_services.bcrypt.checkpw") as mock_check_pw:
            mock_getuser.return_value = User()
            mock_check_pw.return_value = False

            with pytest.raises(HTTPException) as exc:
                update_user_password(1,Password())
                assert exc.value.status_code == 401
                assert exc.value.detail == "Invalid Credentials"

def test_update_password_with_failedtosave():
    with    patch("services.user_services.get_user_by_details") as mock_getuser,\
                    patch("services.user_services.bcrypt.checkpw") as mock_checkpw,\
                    patch("services.user_services.bcrypt.hashpw") as mock_hashpw,\
                    patch("services.user_services.update_password") as mock_updatepassword:
    
                    mock_getuser.return_value = User()
                    mock_checkpw.return_value = True
                    mock_hashpw.return_value = "vlbblb62l3kb6lkqb2libu4629570b79by"
                    mock_updatepassword.return_value = False

                    with pytest.raises(HTTPException) as exc:
                                    update_user_password(1,Password())
                                    assert exc.value.status_code == 500
                                    assert exc.value.detail == "Internal Server Errror"


#Refresh Token Test


refreshtoken = {
     "userid" : 1,
     "exp" : "2026/07/17",
     "type" : "refresh",
     "jti" : 4567
}

class BlackListToken():
     def __int__(self):
          self.id = 1
          self.jti = 4567
          self.expires_at = "2026/08/01"
          self.blocked_at = "2026/07/19"

def test_refresh_token():
     with   patch("services.user_services.get_token") as mock_get_token,\
            patch("services.user_services.create_access_token") as mock_access_token:

            mock_get_token.return_value = None
            mock_access_token.return_value = "fasdft54y.y.43uy64w3ju3.75.j7eszy"

            result = refresh_token(refreshtoken)

            assert result == {"access_token": "fasdft54y.y.43uy64w3ju3.75.j7eszy"}


def test_refresh_token_invalid_type():
     refreshtoken["type"] = "access"
     with   patch("services.user_services.get_token") as mock_get_token :
            mock_get_token.return_value = None

            with pytest.raises(HTTPException) as exc:
                 refresh_token(refreshtoken)
                 assert exc.value.status_code == 401
                 assert  exc.value.detail == "Invalid Token Type"

def test_refersh_token_blacklisted():
     with patch("services.user_services.get_token") as mock_get_token  :
           mock_get_token.return_value = BlackListToken()

           with pytest.raises(HTTPException) as exc:
                refresh_token(refreshtoken)
                assert exc.value.status_code == 401
                assert exc.value.detail == "Token has been revoked"

#Logout Test

token = {
     "userid" : 1,
     "exp" : "2026/07/17",
     "type" : "refresh",
     "jti" : 4567
}

def test_logout():
     with patch("services.user_services.add_token") as mock_add_token:
          mock_add_token.return_value = True

          result = user_logout(token)

          assert result == {"message" : "user logout successfully"}

def test_logout_failedtoadd():
     with patch("services.user_services.add_token") as mock_add_token:
          mock_add_token.return_value = False

          with pytest.raises(HTTPException) as exc:
               user_logout(token)
               assert exc.value.status_code == 500
               assert exc.value.detail == "Internal Server Error"
          