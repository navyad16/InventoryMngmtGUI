from .db_config import connect

def get_inventory(search=None, category_id=None, supplier_id=None):
    conn = connect()
    cur = conn.cursor()
    query = """
        SELECT i.id, i.name, c.name, s.name, i.quantity, i.price
        FROM inventory i
        JOIN category c ON i.category_id = c.id
        JOIN supplier s ON i.supplier_id = s.id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND LOWER(i.name) LIKE %s"
        params.append(f"%{search.lower()}%")
    if category_id and category_id != -1:
        query += " AND i.category_id = %s"
        params.append(category_id)
    if supplier_id and supplier_id != -1:
        query += " AND i.supplier_id = %s"
        params.append(supplier_id)

    query += " ORDER BY i.id"
    cur.execute(query, params)
    data = cur.fetchall()
    conn.close()
    return data

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
