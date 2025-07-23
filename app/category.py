from .db_config import connect

def get_all_categories():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM category ORDER BY name")
    categories = cur.fetchall()
    conn.close()
    return categories

def add_category(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO category (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM category WHERE id = %s", (category_id,))
    conn.commit()
    conn.close()
