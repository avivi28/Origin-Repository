import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv("./data/.env")

poolname="mysqlpool"
poolsize=10

CONFIG={
   "host":'localhost', 
   "user":'root', 
   "password":os.getenv("mysql_password"), 
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
    except:
        db.rollback() #if any errors, undo all data changes
    finally:
        if db.is_connected():
            cursor.close()
        if db:
            db.close()

def queryOne(sql,val):
    try:
        db=connectionPool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql,val)
        return cursor.fetchone()
    except:
        db.rollback()
    finally:
        if db.is_connected():
            cursor.close()
        if db:
            db.close()
            
def uploadData(sql,val):
    try:
        db=connectionPool.get_connection()
        cursor = db.cursor()
        cursor.execute(sql,val)
        db.commit()
        return cursor.fetchone()
    except:
        db.rollback()
    finally:
        if db.is_connected():
            cursor.close()
        if db:
            db.close()