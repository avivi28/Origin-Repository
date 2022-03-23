from flask import *
from model.database import queryOne, alterData
import jwt

true = True
null = None
app.secret_key='my_secret_key'

class UserModel:
    def getUser(self):
        token= request.cookies.get('token')
        if token is not None:
            tokenData= jwt.decode(token, options={"verify_signature": False}) # options for JWT decode
            userInformation={
                "data":tokenData
            }
            return userInformation
        else:
            nullData={
                "data": null}
            return nullData
    
    def signIn(self):
        try:
            json_data=request.get_json()
            email=json_data['email']
            password=json_data['password']
            data=queryOne("SELECT * FROM member WHERE email = %s AND password = %s", (email, password, ))
            if data is not None:
                payload_data={
                    "id":data[0],
                    "name":data[1],
                    "email":data[2]
                }
                token=jwt.encode(
                    payload=payload_data,
                    key=app.secret_key
                )
                sign_in_success={
                    "ok": true
                    }
                return sign_in_success, 200, token
            else:
                sign_in_fail={
                    "error":true,
                    "message":"登入失敗，帳號或密碼錯誤",
                }
                return sign_in_fail, 400
        except:
            server_error={
                    "error":true,
                    "message":"伺服器內部錯誤",
                }
            return server_error, 500
            
    def register(self):
        try:
            json_data=request.get_json() #get back json file from request
            name = json_data["name"]
            email = json_data["email"]
            password = json_data["password"]
            data=queryOne("SELECT * FROM member WHERE email = %s", (email, ))
            if data is not None:
                register_fail={
                    "error":true,
                    "message":"註冊失敗，重複的 Email",
                }
                return register_fail, 400
            else:
                alterData("INSERT INTO member (name, email, password) VALUES (%s, %s, %s)", (name, email, password, ))
                register_success={
                    "ok": true
                    }
            return register_success, 200
        except:   
            server_error={
                    "error":true,
                    "message":"伺服器內部錯誤",
                }
            return server_error, 500
        
    def logOut(self):
        logout_success = {
                "ok": true
                }
        return logout_success

user_model=UserModel()