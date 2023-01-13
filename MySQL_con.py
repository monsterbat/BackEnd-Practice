import mysql.connector
# .env 
from dotenv import load_dotenv
import os
load_dotenv()
MySQL_host = os.getenv("MySQL_host")
MySQL_user = os.getenv("MySQL_user")
MySQL_password = os.getenv("MySQL_password")
MySQL_database = os.getenv("MySQL_database")

# MySQL connect and input/output
def get_connect():
    return mysql.connector.connect(
        host = MySQL_host,
        user = MySQL_user,
        password = MySQL_password,
        database = MySQL_database,
        charset="utf8"
)

def query_data_read(sql_command):
    conn=get_connect()
    try:
        cursor=conn.cursor(dictionary=True)
        cursor.execute(sql_command)
        return cursor.fetchall()
    finally:
        conn.close()

def query_data(sql_command,input):
    conn=get_connect()
    try:
        cursor=conn.cursor(dictionary=True)
        cursor.execute(sql_command,input)
        return cursor.fetchall()
    finally:
        conn.close()

def insert_or_update_data(sql_command,input):
    conn=get_connect()
    try:
        cursor=conn.cursor(dictionary=True)
        cursor.execute(sql_command,input)
        conn.commit()
        return cursor.fetchall()
    finally:
        conn.close()
