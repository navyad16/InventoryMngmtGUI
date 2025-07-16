from db import get_connection
def get_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM categories;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
