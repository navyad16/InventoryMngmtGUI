import psycopg2

def connect():
    return psycopg2.connect(
        host="localhost",
        database="inventory_db",     # Change to your DB name
        user="postgres",             # Change to your username
        password=""     # Change to your password
    )

