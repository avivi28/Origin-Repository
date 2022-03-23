from flask import *
from model.user import user_model

user_api=Blueprint("user",__name__)

@user_api.route("/api/user", methods=['GET','POST','PATCH','DELETE'])
def get():
    if request.method == 'GET':
        get_result = user_model.getUser()
        return jsonify(get_result)
    
    elif request.method == 'POST':
        return_result = user_model.register()
        post_result = return_result[0]
        return_status = return_result[1]
        if return_status == 200:
            return jsonify(post_result)
        elif return_status == 400:
            return jsonify(post_result), 400
        else:
            return jsonify(post_result), 500
        
    elif request.method == 'PATCH':
        patch_result = user_model.signIn()
        json_result = patch_result[0]
        token = patch_result[1]
        if patch_result is not None:
            resp=make_response()
            resp.set_cookie(key="token", value=token)
            return jsonify(json_result), resp
        elif patch_result is None:
            return jsonify(json_result), 400
        else:
            return jsonify(json_result), 500
    
    elif request.method == 'DELETE':
        delete_result = user_model.logOut()
        resp=Response()
        resp.set_cookie(key="token", value='', expires=0)
        return jsonify(delete_result), resp