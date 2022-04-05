from flask import *
from model.database import uploadData
import requests
import jwt
import time

true = True
false = False

class ordersModel:
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
                'x-api-key': 'partner_74Q0eA51ATQu8DnNqcbz5lD1iHIFpjGR2aTtsvpGTfHcCTebkyw1lXvD',
                'Content-Type': 'application/json',
            }

            prime_data = {
                "prime": input_prime,
                "partner_key": "partner_74Q0eA51ATQu8DnNqcbz5lD1iHIFpjGR2aTtsvpGTfHcCTebkyw1lXvD",
                "merchant_id": "BearPawCompany_ESUN",
                "details":"TapPay Test",
                "amount": input_amount,
                "cardholder": {
                    "phone_number": input_phone,
                    "name": input_name,
                    "email": input_email,
                },
                "remember": false
            }

            token= request.cookies.get('token')
            if token is not None:
                tokenData= jwt.decode(token, options={"verify_signature": False})
                input_userId = tokenData['id']

                sql = "INSERT INTO orders (id, price, date, time, payment_status, attraction_id, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (order_number, input_amount, input_date, input_time, "未付款", input_attractionId, input_userId, )
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
                    uploadData("UPDATE orders SET payment_status = %s WHERE id = %s", ('已付款', order_number,))
                    payment_sql = "INSERT INTO payment (order_number, status, price, attraction_id, user_id) VALUES (%s, %s, %s, %s, %s)"
                    payment_val = (order_number, prime_status, input_amount, input_attractionId, input_userId, )
                    uploadData(payment_sql, payment_val)

                    return return_TapPaymessage, 200
                else:
                    data_error = {
                        "error": true,
                        "message": prime_msg
                    }
                    return data_error, 400
            else:
                login_error = {
                    "error": true,
                    "message": "未登入系統，拒絕存取"
                }
                return login_error, 403
        except:
            server_error={
                    "error":true,
                    "message":"伺服器內部錯誤",
                }
            return server_error, 500

orders_model=ordersModel()