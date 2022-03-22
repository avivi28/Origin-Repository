from flask import *
from model.user import user_model

user_api=Blueprint("user",__name__)

@user_api.route("/api/user", methods=['GET'])
def get():
    result = user_model.getUser()
    return jsonify(result)

@user_api.route("/api/user", methods=['POST'])
def post():
    result = user_model.register()
    if result is not None:
        return jsonify(result), 400
    elif result is None:
        return jsonify(result)
    else:
        return jsonify(result), 500

@user_api.route("/api/user", methods=['PATCH'])
def patch():
    result = user_model.signIn()
    json_result = result[0]
    token = result[1]
    if result is not None:
        resp=make_response()
        resp.set_cookie(key="token", value=token)
        return jsonify(json_result), resp
    elif result is None:
        return jsonify(json_result), 400
    else:
        return jsonify(json_result), 500
    
@user_api.route("/api/user", methods=['DELETE'])
def delete():
    result = user_model.logOut()
    resp=Response()
    resp.set_cookie(key="token", value='', expires=0)
    return jsonify(result), resp