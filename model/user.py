from flask import *
from model.database import query_one, upload_data
import jwt
from flask_bcrypt import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import re  # Regex

load_dotenv("./data/.env")

true = True
null = None
app.secret_key = os.getenv("secret_key")


class UserModel:
    def get_user(self):
        token = request.cookies.get('token')
        if token is not None:
            # options for JWT decode
            tokenData = jwt.decode(token, options={"verify_signature": False})
            return {
                "data": tokenData
            }
        else:
            return {
                "data": null}

    def sign_in(self):
        try:
            json_data = request.get_json()
            input_email = json_data['email']
            input_password = json_data['password']
            email_format_check = re.search(
                "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", input_email)
            if email_format_check:
                data = query_one(
                    "SELECT * FROM member WHERE email = %s", (input_email, ))
                hashed_password = data['password']
                # compare hashed_password with input_password
                checked_password = check_password_hash(
                    hashed_password, input_password)
                if data is not None:
                    if checked_password is True:
                        payload_data = {
                            "id": data['member_id'],
                            "name": data['name'],
                            "email": data['email']
                        }
                        token = jwt.encode(
                            payload=payload_data,
                            key=app.secret_key
                        )
                        return {"ok": true}, 200, token
                else:
                    return {
                        "error": true,
                        "message": "登入失敗，帳號或密碼錯誤",
                    }, 400
            else:
                return {
                    "error": true,
                    "message": "資料格式錯誤",
                }, 400
        except:
            return {
                "error": true,
                "message": "伺服器內部錯誤",
            }, 500, json_data

    def register(self):
        try:
            json_data = request.get_json()  # get back json file from request
            input_name = json_data["name"]
            input_email = json_data["email"]
            input_password = json_data["password"]
            hashed_password = generate_password_hash(input_password)
            email_format_check = re.search(
                "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", input_email)
            # prevent any special characters
            name_format_check = re.search("[a-zA-Z0-9]", input_name)
            if email_format_check and name_format_check:
                data = query_one(
                    "SELECT * FROM member WHERE email = %s", (input_email, ))
                if data is not None:
                    return {
                        "error": true,
                        "message": "註冊失敗，重複的 Email",
                    }, 400
                else:
                    upload_data("INSERT INTO member (name, email, password) VALUES (%s, %s, %s)", (
                        input_name, input_email, hashed_password, ))
                    return {"ok": true}, 200
            else:
                return {
                    "error": true,
                    "message": "資料格式錯誤",
                }, 400
        except:
            return {
                "error": true,
                "message": "伺服器內部錯誤",
            }, 500

    def log_out(self):
        return {"ok": true}


user_model = UserModel()
