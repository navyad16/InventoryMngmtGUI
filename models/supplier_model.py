from db import get_connection
def get_suppliers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * from suppliers;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
