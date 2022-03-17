from flask import *
from model.id import id_model

id_api=Blueprint("id",__name__)

@id_api.route("/api/attraction/<attractionId>") #this is path parameter
def getDataById(attractionId):
    result = id_model.getId(attractionId)
    try:
        return jsonify(result)
    except TypeError: 
        return jsonify(result), 400
    except:
        return jsonify(result), 500