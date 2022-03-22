from flask import *
from model.database import queryOne, alterData

true = True

class UserModel:
    def getUser(self):
        # flask cookies get 
        register_data = request.values
        id= register_data["id"]
        userData=queryOne("SELECT * FROM member WHERE id = %s", (id, ))
        userInformation={
            "data": {
            "id": userData[0],
            "name": userData[1],
            "email": userData[2]
        }}
        return userInformation
    
    def signIn(self):
        try:
            signin_data = request.values
            email=signin_data['email']
            password=signin_data['password']
            data=queryOne("SELECT * FROM member WHERE email = %s AND password = %s", (email, password, ))
            if data is not None:
                sign_in_success={
                    "ok": true
                    }
                return sign_in_success
            else:
                sign_in_fail={
                    "error":true,
                    "message":"登入失敗，帳號或密碼錯誤",
                }
                return sign_in_fail
        except:
            server_error={
                    "error":true,
                    "message":"伺服器內部錯誤",
                }
            return server_error     
            
    def register(self):
        try:
            register_data = request.values
            name= register_data["name"]
            email= register_data["email"]
            password= register_data["password"]
            data=queryOne("SELECT * FROM member WHERE email = %s", (email, ))
            if data is not None:
                register_fail={
                    "error":true,
                    "message":"註冊失敗，重複的 Email",
                }
                return register_fail
            else:
                alterData("INSERT INTO member (name, email, password) VALUES (%s, %s, %s)", (name, email, password, ))
                register_success={
                    "ok": true
                    }
            return register_success
        except:   
            server_error={
                    "error":true,
                    "message":"伺服器內部錯誤",
                }
            return server_error   
        
    def logOut(self):
        logout_success = {
                "ok": true
                }
        return logout_success

user_model=UserModel()