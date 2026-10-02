from database import get_db_connection

def get_or_create_user(ip_address):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ip_address FROM users WHERE ip_address = %s;", (ip_address,))
    user = cur.fetchone()
    if not user:
        cur.execute("INSERT INTO users (ip_address) VALUES (%s);", (ip_address,))
        conn.commit()
    cur.close()
    conn.close()
    return ip_address

def get_chat_history(ip_address, limit=10):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT role, content FROM chat_history 
        WHERE ip_address = %s 
        ORDER BY id DESC LIMIT %s;
    """, (ip_address, limit))
    rows = cur.fetchall()[::-1]
    cur.close()
    conn.close()
    return rows

def save_chat_message(ip_address, role, content):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO chat_history (ip_address, role, content) 
        VALUES (%s, %s, %s);
    """, (ip_address, role, content))
    conn.commit()
    cur.close()
    conn.close()
  
