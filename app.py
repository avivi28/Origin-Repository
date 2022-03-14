from flask import *
from controller.attraction import attractions_api
from controller.id import id_api

app=Flask(__name__,template_folder='templates',static_folder='static')
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

app.register_blueprint(attractions_api)     
app.register_blueprint(id_api)      
    
# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

#API

# @app.route("/api/attraction/<attractionId>") #this is path parameter
# def getDataById(attractionId):
#     try:
#         attractionId=int(attractionId)
#         Id_data=queryOne("SELECT * FROM attractions WHERE id = %s", (attractionId,))

#         id=Id_data[0]
#         name=Id_data[1]
#         category=Id_data[2]
#         description=Id_data[3]
#         address=Id_data[4]
#         transport=Id_data[5]
#         mrt=Id_data[6]
#         latitude=Id_data[7]
#         longitude=Id_data[8]
#         images_data=Id_data[9].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")

#         success_idData_return={
#             "data": {
#                 "id": id,
#                 "name": name,
#                 "category": category,
#                 "description": description,
#                 "address": address,
#                 "transport": transport,
#                 "mrt": mrt,
#                 "latitude": latitude,
#                 "longitude": longitude,
#                 "images": images_data
#                 }
#             }
#         return jsonify(success_idData_return)
#     except TypeError: 
#             true = True
#             error_message={
#                 "error": true,
#                 "message": "Wrong Request ID!"
#             }
#             return jsonify(error_message), 400
#     except:
#             true = True
#             error_message={
#                 "error": true,
#                 "message": "Server Side Error!"
#             }
#             return jsonify(error_message), 500

if __name__=='__main__':
    app.debug=True
    app.run(port=3000)