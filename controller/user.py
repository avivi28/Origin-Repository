from flask import *
from model.user import user_model

user_api=Blueprint("user",__name__)

@user_api.route("/api/user", methods=['GET','POST','PATCH','DELETE'])
def get():
    if request.method == 'GET':
        get_result = user_model.get_user()
        return jsonify(get_result)
    
    elif request.method == 'POST':
        return_result = user_model.register()
        post_result = return_result[0]
        register_status = return_result[1]
        if register_status == 200:
            return jsonify(post_result)
        elif register_status == 400:
            return jsonify(post_result), 400
        else:
            return jsonify(post_result), 500
        
    elif request.method == 'PATCH':
        patch_result = user_model.sign_in()
        json_result = patch_result[0]
        signin_status = patch_result[1]
        if signin_status == 200:
            token = patch_result[2]
            resp=make_response(jsonify(json_result))
            resp.set_cookie(key="token", value=token)
            return resp
        elif signin_status == 400:
            return jsonify(json_result), 400
        else:
            return jsonify(json_result), 500
    
    elif request.method == 'DELETE':
        delete_result = user_model.log_out()
        resp=make_response(jsonify(delete_result))
        resp.set_cookie(key="token", value='', expires=0)
        return resp