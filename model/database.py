import mysql.connector.pooling
import os
from dotenv import load_dotenv

load_dotenv()

poolname = "mysqlpool"
poolsize = 10

print(os.getenv("mysql_host"))

CONFIG = {
    "host": os.getenv("mysql_host"),
    "user":  os.getenv("mysql_root"),
    "password": os.getenv("mysql_password"),
    "database": os.getenv("mysql_database"),
}

db = mysql.connector.connect(pool_name=poolname, pool_size=poolsize,
                             pool_reset_session=True, auth_plugin='mysql_native_password', **CONFIG)
connectionPool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name=poolname, pool_size=poolsize, pool_reset_session=True, auth_plugin='mysql_native_password', **CONFIG)  # connection pool


def query_all(sql, val):
    try:
        db = connectionPool.get_connection()  # get data from connection pool
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, val)
        return cursor.fetchall()
    except:
        db.rollback()  # if any errors, undo all data changes
    finally:
        if db.is_connected():
            cursor.close()
        db.close()


def query_one(sql, val):
    try:
        db = connectionPool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, val)
        return cursor.fetchone()
    except mysql.connector.Error as error:
        print("error", format(error))
        db.rollback()  # any errors, undo all changes
    finally:
        if db.is_connected():
            cursor.close()
        db.close()


def upload_data(sql, val):
    try:
        db = connectionPool.get_connection()
        cursor = db.cursor()
        cursor.execute(sql, val)
        db.commit()
        return cursor.fetchone()
    except mysql.connector.Error as error:
        print("error", format(error))
        db.rollback()  # any errors, undo all changes
    finally:
        if db.is_connected():
            cursor.close()
        db.close()
