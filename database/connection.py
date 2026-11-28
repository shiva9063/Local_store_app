import mysql.connector

def get_connection():
    conn=mysql.connector.connect(
        host='localhost',
        user='root',
        password='shiva1432',
        database='local_store_db'
    ) 
    return conn 
