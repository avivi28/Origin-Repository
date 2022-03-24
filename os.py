import os

os.environ["mysql_password"]="password"
password = os.environ.get("mysql_password")

print(type(password))

bear = os.environ
