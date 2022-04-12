from flask import *
from model.database import queryOne, uploadData
import jwt
from flask_bcrypt import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv("./data/.env")

true = True
null = None
app.secret_key= os.getenv("secret_key")

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
            input_email=json_data['email']
            input_password=json_data['password']
            data=queryOne("SELECT * FROM member WHERE email = %s", (input_email, ))
            hashed_password=data['password']
            checked_password= check_password_hash(hashed_password, input_password) # compare hashed_password with input_password
            if data is not None:
                if checked_password is True:
                    payload_data={
                        "id":data['member_id'],
                        "name":data['name'],
                        "email":data['email']
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
            return server_error, 500, json_data
            
    def register(self):
        try:
            json_data=request.get_json() #get back json file from request
            input_name = json_data["name"]
            input_email = json_data["email"]
            input_password = json_data["password"]
            hashed_password = generate_password_hash(input_password)
            data=queryOne("SELECT * FROM member WHERE email = %s", (input_email, ))
            if data is not None:
                register_fail={
                    "error":true,
                    "message":"註冊失敗，重複的 Email",
                }
                return register_fail, 400
            else:
                uploadData("INSERT INTO member (name, email, password) VALUES (%s, %s, %s)", (input_name, input_email, hashed_password, ))
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