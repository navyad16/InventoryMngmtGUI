# app/models.py

from .db_config import connect

# ------------------ CATEGORY ------------------

def get_all_categories():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM category ORDER BY name")
    categories = cur.fetchall()
    conn.close()
    return categories

# ------------------ SUPPLIER ------------------

def get_all_suppliers():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM supplier ORDER BY name")
    suppliers = cur.fetchall()
    conn.close()
    return suppliers

# ------------------ INVENTORY ------------------

def get_all_inventory():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT i.id, i.name, c.name, s.name, i.quantity, i.price
        FROM inventory i
        JOIN category c ON i.category_id = c.id
        JOIN supplier s ON i.supplier_id = s.id
        ORDER BY i.id
    """)
    items = cur.fetchall()
    conn.close()
    return items

def add_inventory(name, category_id, supplier_id, quantity, price):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO inventory (name, category_id, supplier_id, quantity, price)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, category_id, supplier_id, quantity, price))
    conn.commit()
    conn.close()

def update_inventory(item_id, name, category_id, supplier_id, quantity, price):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE inventory
        SET name=%s, category_id=%s, supplier_id=%s, quantity=%s, price=%s
        WHERE id=%s
    """, (name, category_id, supplier_id, quantity, price, item_id))
    conn.commit()
    conn.close()

def delete_inventory(item_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()
