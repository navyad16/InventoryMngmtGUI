from .db_config import connect

def get_all_suppliers():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM supplier ORDER BY name")
    suppliers = cur.fetchall()
    conn.close()
    return suppliers

def add_supplier(name, contact):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO supplier (name, contact) VALUES (%s, %s)", (name, contact))
    conn.commit()
    conn.close()

def delete_supplier(supplier_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM supplier WHERE id = %s", (supplier_id,))
    conn.commit()
    conn.close()
