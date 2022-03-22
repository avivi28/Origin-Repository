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
    if result is not None:
        return jsonify(result)
    elif result is None:
        return jsonify(result), 400
    else:
        return jsonify(result), 500
    
@user_api.route("/api/user", methods=['DELETE'])
def delete(): #session = 0
    result = user_model.logOut()
    return jsonify(result)