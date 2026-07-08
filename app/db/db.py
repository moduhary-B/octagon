import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


DB_CONFIG = {
    'dbname': 'octagon',
    'user': 'octagon',
    'password': '12345',
    'host': 'localhost',
    'port': 5432
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

@contextmanager
def get_cursor(commit=False):
    conn = get_connection()
    if not conn:
        raise Exception("Не удалось подключиться к БД")
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def init_db():
    with get_cursor(commit=True) as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL UNIQUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2),
                url VARCHAR(500),
                category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL
            )
        """)
        print("Таблицы успешно созданы (или уже существуют)")

if __name__ == "__main__":
    init_db()