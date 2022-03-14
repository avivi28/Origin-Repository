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

if __name__=='__main__':
    app.debug=True
    app.run(port=3000)