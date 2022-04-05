from flask import *
from model.orders import orders_model

orders_api=Blueprint("orders",__name__)

@orders_api.route("/api/orders", methods=['POST'])
def post():
    return_result = orders_model.postorders()
    post_result = return_result[0]
    post_status = return_result[1]
    if post_status == 200:
        return jsonify(post_result)
    elif post_status == 400:
        return jsonify(post_result), 400
    elif post_status == 403:
        return jsonify(post_result), 403
    else:
        return jsonify(post_result), 500