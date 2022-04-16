from flask import *
from model.database import query_one, upload_data
import jwt
import re
import traceback

true = True
null = None


class bookingModel:
    def get_booking(self):
        token = request.cookies.get('token')
        if token is not None:
            tokenData = jwt.decode(token, options={"verify_signature": False})
            token_userId = tokenData["id"]
            booking_data = query_one(
                "SELECT * FROM booking WHERE user_id = %s ORDER BY booking_id DESC LIMIT 1", (token_userId, ))
            if booking_data is not None:
                attraction_id = booking_data['attraction_id']
                attraction_data = query_one(
                    "SELECT * FROM attractions WHERE attractions_id = %s", (attraction_id, ))
                image_data = attraction_data['images'].split(
                    ',')[0].replace("[", "").replace("'", "", 2)

                get_success = {
                    "data": {
                        "attraction": {
                            "id": attraction_id,
                            "name": attraction_data['attractions_name'],
                            "address": attraction_data['address'],
                            "image": image_data
                        },
                        "date": booking_data['booking_date'],
                        "time": booking_data['booking_time'],
                        "price": booking_data['price']
                    }
                }
                return get_success, 200
            else:
                return {"data": null}, 200
        else:
            return {
                "error": true,
                "message": "未登入系統，拒絕存取"
            }, 403

    def post_booking(self):
        try:
            json_data = request.get_json()
            input_attractionId = json_data["attractionId"]
            input_date = json_data["date"]
            input_time = json_data["time"]
            input_price = json_data["price"]

            input_date_check = re.search("[0-9|-]", input_date)
            input_time_check = re.search("[\u4e00-\u9fff|0-9]", input_date)

            if input_date_check and input_time_check:
                token = request.cookies.get('token')
                tokenData = jwt.decode(
                    token, options={"verify_signature": False})
                token_userId = tokenData["id"]

                if token is not None:
                    upload_data("INSERT INTO booking (attraction_id, user_id, booking_date, booking_time, price) VALUES (%s, %s, %s, %s, %s)", (
                        input_attractionId, token_userId, input_date, input_time, input_price, ))
                    return {"ok": true}, 200
                elif token is None:
                    return {
                        "error": true,
                        "message": "未登入系統，拒絕存取"
                    }, 403
                else:
                    return {
                        "error": true,
                        "message": "建立失敗，輸入不正確或其他原因"
                    }, 400
            else:
                return {
                    "error": true,
                    "message": "資料格式錯誤",
                }, 400
        except Exception as e:
            traceback.print_exc()
            return {
                "error": true,
                "message": "伺服器內部錯誤",
            }, 500

    def delete_booking(self):
        token = request.cookies.get('token')
        tokenData = jwt.decode(token, options={"verify_signature": False})
        token_userId = tokenData["id"]

        if token is not None:
            upload_data("DELETE FROM booking WHERE user_id = %s",
                        (token_userId, ))
            return {"ok": true}, 200
        else:
            return {
                "error": true,
                "message": "自訂的錯誤訊息"
            }, 403


booking_model = bookingModel()
