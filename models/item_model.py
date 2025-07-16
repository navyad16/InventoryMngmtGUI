from db import get_connection

def get_all_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT items.id, items.name, categories.name, suppliers.name, items.quantity
        FROM items
        JOIN categories ON items.category_id = categories.id
        JOIN suppliers ON items.supplier_id = suppliers.id
        ORDER BY items.id;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_item(name, category_id, supplier_id, quantity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO items (name, category_id, supplier_id, quantity)
        VALUES (%s, %s, %s, %s);
    """, (name, category_id, supplier_id, quantity))
    conn.commit()
    cur.close()
    conn.close()

def update_item(item_id, name, category_id, supplier_id, quantity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE items
        SET name = %s, category_id = %s, supplier_id = %s, quantity = %s
        WHERE id = %s;
    """, (name, category_id, supplier_id, quantity, item_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_item(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s;", (item_id,))
    conn.commit()
    cur.close()
    conn.close()

def search_items(keyword):
    conn = get_connection()
    cur = conn.cursor()
    search_query = f"%{keyword}%"
    cur.execute("""
        SELECT items.id, items.name, categories.name, suppliers.name, items.quantity
        FROM items
        JOIN categories ON items.category_id = categories.id
        JOIN suppliers ON items.supplier_id = suppliers.id
        WHERE items.name ILIKE %s
        ORDER BY items.id;
    """, (search_query,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

