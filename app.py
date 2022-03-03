from urllib.error import HTTPError
from flask import *
import mysql.connector
from mysql.connector import pooling


poolname="mysqlpool"
poolsize=3

connectionpool=mysql.connector.pooling.MySQLConnectionPool(pool_name=poolname,pool_size=poolsize, pool_reset_session=True, host='localhost', user='root', password="password", database='travel')
db = connectionpool.get_connection()
cursor = db.cursor()

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

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
@app.route("/api/attractions")
def getData():
    try:
        page=request.args.get("page",0)
        page=int(page)
        limit_page=page*12
        keyword=request.args.get("keyword")

        if keyword is not None:
            keyword="%"+keyword+"%"
            cursor.execute("SELECT * FROM attractions WHERE name LIKE %s LIMIT 12 OFFSET %s", (keyword, limit_page,))
            data=cursor.fetchall()
            data=list(data)
            if len(data)>=12:
                next_page=page+1
            else:
                null=None
                next_page=null
            success_data_return={
            "nextPage": next_page,
            "data": []
            }
            
            for x in range(0,len(data)):
                id=data[x][0]
                name=data[x][1]
                category=data[x][2]
                description=data[x][3]
                address=data[x][4]
                transport=data[x][5]
                mrt=data[x][6]
                latitude=data[x][7]
                longitude=data[x][8]
                images_data=data[x][9].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")
                
                temp = {
                    "id": id,
                    "name": name,
                    "category": category,
                    "description": description,
                    "address": address,
                    "transport": transport,
                    "mrt": mrt,
                    "latitude": latitude,
                    "longitude": longitude,
                    "images": images_data
                }
                success_data_return["data"].append(temp)
            return jsonify(success_data_return)
        else:
            cursor.execute("SELECT * FROM attractions LIMIT 12 OFFSET %s", (limit_page,))
            data=cursor.fetchall()
            data=list(data)
            if len(data)>=12:
                next_page=page+1
            else:
                null=None
                next_page=null
            success_data_return={
            "nextPage": next_page,
            "data": []
            }
            
            for x in range(0,len(data)):
                id=data[x][0]
                name=data[x][1]
                category=data[x][2]
                description=data[x][3]
                address=data[x][4]
                transport=data[x][5]
                mrt=data[x][6]
                latitude=data[x][7]
                longitude=data[x][8]
                images_data=data[x][9].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")
                
                temp = {
                    "id": id,
                    "name": name,
                    "category": category,
                    "description": description,
                    "address": address,
                    "transport": transport,
                    "mrt": mrt,
                    "latitude": latitude,
                    "longitude": longitude,
                    "images": images_data
                }
                success_data_return["data"].append(temp) #要一步步塞data進去
            return jsonify(success_data_return)
    except HTTPError as e:
        if e.response.status.code==500:
            true = True
            error_message={
                "error": true,
                "message": "Server Side Error!"
            }
            return jsonify(error_message), 500

@app.route("/api/attraction/<attractionId>") #this is path parameter
def getDataById(attractionId):
    try:
        attractionId=int(attractionId)
        cursor.execute("SELECT * FROM attractions WHERE id = %s", (attractionId,))
        Id_data=cursor.fetchone()
        success_idData_return={
            "data": []
            }

        id=Id_data[0]
        name=Id_data[1]
        category=Id_data[2]
        description=Id_data[3]
        address=Id_data[4]
        transport=Id_data[5]
        mrt=Id_data[6]
        latitude=Id_data[7]
        longitude=Id_data[8]
        images_data=Id_data[9].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")

        temp = {
            "id": id,
            "name": name,
            "category": category,
            "description": description,
            "address": address,
            "transport": transport,
            "mrt": mrt,
            "latitude": latitude,
            "longitude": longitude,
            "images": images_data
        }
        success_idData_return["data"].append(temp)
        return jsonify(success_idData_return)
    except HTTPError as e:
        if e.response.status.code==400:
            true = True
            error_message={
                "error": true,
                "message": "Request Error!"
            }
            return jsonify(error_message), 500
        elif e.response.status.code==500:
            true = True
            error_message={
                "error": true,
                "message": "Server Side Error!"
            }
            return jsonify(error_message), 500
    
if __name__=='__main__':
    app.debug=True
    app.run(port=3000)