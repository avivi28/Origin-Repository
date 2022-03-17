import mysql.connector
from mysql.connector import pooling

poolname="mysqlpool"
poolsize=3

CONFIG={
   "host":'localhost', 
   "user":'root', 
   "password":"password", 
   "database":'travel',
}
db=mysql.connector.connect(pool_name=poolname,pool_size=poolsize, pool_reset_session=True, auth_plugin='mysql_native_password',**CONFIG)
connectionPool=mysql.connector.pooling.MySQLConnectionPool(pool_name=poolname,pool_size=poolsize, pool_reset_session=True, auth_plugin='mysql_native_password',**CONFIG)
db=connectionPool.get_connection()

def queryAll(sql,val):
    try:
        db=connectionPool.get_connection()
        cursor = db.cursor()
        cursor.execute(sql,val)
        return cursor.fetchall()
    finally:
        if db.is_connected():
            cursor.close()
        if db:
            db.close()

def queryOne(sql,val):
    try:
        db=connectionPool.get_connection()
        cursor = db.cursor()
        cursor.execute(sql,val)
        return cursor.fetchone()
    finally:
        if db.is_connected():
            cursor.close()
        if db:
            db.close()