from distutils.log import error
from flask import *
from model.database import queryOne, uploadData
import requests
import jwt
import time
import os
from dotenv import load_dotenv

load_dotenv("./data/.env")

true = True
false = False

class ordersModel:
    def getorders(self, orderNumber):
        token= request.cookies.get('token')
        if token is not None:
            order_number = str(orderNumber)
            order_data = queryOne("SELECT * FROM orders INNER JOIN member ON orders.user_id = member.id INNER JOIN attractions ON orders.attraction_id = attractions.id WHERE orders.payment_number = %s", (order_number, ))
            image_data = order_data[22]
            return_order_number = {
                "data": {
                    "number": order_number,
                    "price": order_data[2],
                    "trip": {
                    "attraction": {
                        "id": order_data[7],
                        "name": order_data[14],
                        "address": order_data[17],
                        "image": image_data.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")[0]
                    },
                    "date": order_data[3],
                    "time": order_data[4]
                    },
                    "contact": {
                    "name": order_data[10],
                    "email": order_data[11],
                    "phone": order_data[6]
                    },
                    "status": order_data[5],
                }
            }
            return return_order_number, 200
        else:
            return {"error": true, "message": "未登入系統，拒絕存取"}, 403
    
    def postorders(self):
        try:
            local_time = str(time.strftime('%Y%m%D%H%M%S', time.localtime(time.time())).replace('/','')+str(time.time()).replace(',','')[-7:])
            order_number = local_time

            json_data = request.get_json()
            order_data = json_data["order"]
            input_prime = json_data["prime"]

            input_amount = order_data["price"]
            input_name = order_data["contact"]["name"]
            input_phone = order_data["contact"]["phone"]
            input_email = order_data["contact"]["email"]

            attraction_data = order_data["trip"]
            input_date = attraction_data["date"]
            input_time = attraction_data["time"]
            input_attractionId = attraction_data["attraction"]["id"]

            headers = {
                'x-api-key': os.getenv("parent_key"),
                'Content-Type': 'application/json',
            }

            prime_data = {
                "prime": input_prime,
                "partner_key": os.getenv("parent_key"),
                "merchant_id": os.getenv("merchant_id"),
                "details":"TapPay Test",
                "amount": input_amount,
                "cardholder": {
                    "phone_number": input_phone,
                    "name": input_name,
                    "email": input_email,
                },
            }

            token= request.cookies.get('token')
            if token is not None:
                tokenData= jwt.decode(token, options={"verify_signature": False})
                input_userId = tokenData['id']

                sql = "INSERT INTO orders (payment_number, price, date, time, payment_status, user_phone, attraction_id, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (order_number, input_amount, input_date, input_time, 1, input_phone, input_attractionId, input_userId, )
                uploadData(sql,val)
                
                prime_response = requests.post("https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime", headers = headers, data = json.dumps(prime_data)).json() #get the json content & convert into dictionary
                prime_status = prime_response["status"]
                prime_msg = prime_response["msg"]

                return_TapPaymessage = {
                    "data": {
                        "number": order_number,
                        "payment": {
                            "status": prime_status,
                            "message": prime_msg
                        }
                    }
                }

                if prime_status == 0:
                    uploadData("UPDATE orders SET payment_status = %s WHERE payment_number = %s", (0, order_number,))
                    payment_sql = "INSERT INTO payment (order_number, status, price, attraction_id, user_id) VALUES (%s, %s, %s, %s, %s)"
                    payment_val = (order_number, prime_status, input_amount, input_attractionId, input_userId, )
                    uploadData(payment_sql, payment_val)
                    print (return_TapPaymessage)

                    return return_TapPaymessage, 200

                else:
                    return {"error": true,"message": prime_msg}, 400

            else:
                return {"error": true,"message": "未登入系統，拒絕存取"}, 403

        except Exception as e:
            return {"error": true,"message": "伺服器內部錯誤"}, 500

orders_model=ordersModel()