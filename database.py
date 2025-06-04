import os
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    result = urlparse(db_url)
    return psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

def create_tables():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY,
                    chat_id BIGINT UNIQUE NOT NULL
                )
            """)
            conn.commit()

def add_user(username, chat_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (username, chat_id) VALUES (%s, %s)", (username, chat_id))
                conn.commit()
        return True
    except psycopg2.errors.UniqueViolation:
        return False

def get_username(chat_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT username FROM users WHERE chat_id = %s", (chat_id,))
            result = cur.fetchone()
            return result[0] if result else None

def get_chat_id(username):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT chat_id FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            return result[0] if result else None
