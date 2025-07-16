#Database Table DDL (PostgreSQL)
#Make sure your schema is created:

"""CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    contact TEXT
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INT REFERENCES categories(id),
    supplier_id INT REFERENCES suppliers(id),
    quantity INT DEFAULT 0 CHECK (quantity >= 0)
);"""

import psycopg2
import configparser

def get_connection():
    config = configparser.ConfigParser()
    config.read('config.ini')
    db = config['postgresql']
    return psycopg2.connect(
        host=db['host'],
        database=db['database'],
        user=db['user'],
        password=db['password'],
        port=db['port']
    )


