from audioop import add
import json
import mysql.connector
from mysql.connector import pooling

poolname="mysqlpool"
poolsize=3

connectionpool=mysql.connector.pooling.MySQLConnectionPool(pool_name=poolname,pool_size=poolsize, pool_reset_session=True, host='localhost', user='root', password="password", database='travel', auth_plugin='mysql_native_password')
db = connectionpool.get_connection()
cursor = db.cursor()

f=open('taipei-attractions.json', encoding="utf-8")
data=json.load(f)
sorted_result=data['result']['results']
for all_data in sorted_result:
    id=all_data["_id"]
    name=all_data["stitle"]
    cat=all_data["CAT2"]
    description=all_data["xbody"]
    address=all_data["address"][0:3]+all_data["address"][5:]
    transport=all_data["info"]
    mrt=all_data["MRT"]
    latitude=all_data["latitude"]
    longitude=all_data["longitude"]
    image=all_data["file"]
    image=image.split("https")
    sorted_image=[]
    for x in image:
        if x.endswith(".jpg") or x.endswith(".JPG"):
            sorted_image.append("https"+x)
    sorted_image=str(sorted_image)
    sql="INSERT INTO attractions (id, name, category, description, address, transport, mrt, latitude, longitude, images) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(id, name, cat, description, address, transport, mrt, latitude, longitude, sorted_image)
    cursor.execute(sql,val)
    db.commit()
f.close() # close the file after used