from flask import *
from model.attraction import attraction_model

attractions_api=Blueprint("attractions",__name__)

@attractions_api.route("/api/attractions")
def handle():
    result = attraction_model.get()
    if result == None:
        error_message = result
        return jsonify(error_message), 500
    else:
        success_data_return = attraction_model.get()
        return jsonify(success_data_return)