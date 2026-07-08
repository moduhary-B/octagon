from app.db.db import get_cursor
from app.db.models import Category, Book



def create_category(title):
    #Создание категории
    with get_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO categories (title) VALUES (%s) RETURNING id, title",
            (title,)
        )
        result = cursor.fetchone()
        return Category.from_dict(result) if result else None

def get_category(category_id):
    #Получение категории по ID
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT id, title FROM categories WHERE id = %s",
            (category_id,)
        )
        result = cursor.fetchone()
        return Category.from_dict(result) if result else None

def get_category_by_title(title):
    #Получение категории по названию
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT id, title FROM categories WHERE title = %s",
            (title,)
        )
        result = cursor.fetchone()
        return Category.from_dict(result) if result else None

def get_all_categories():
    #Получение всех категорий
    with get_cursor() as cursor:
        cursor.execute("SELECT id, title FROM categories ORDER BY title")
        results = cursor.fetchall()
        return [Category.from_dict(row) for row in results]

def update_category(category_id, title):
    #Обновление категории
    with get_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE categories SET title = %s WHERE id = %s RETURNING id, title",
            (title, category_id)
        )
        result = cursor.fetchone()
        return Category.from_dict(result) if result else None

def delete_category(category_id):
    #Удаление категории
    with get_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE books SET category_id = NULL WHERE category_id = %s",
            (category_id,)
        )
        cursor.execute(
            "DELETE FROM categories WHERE id = %s RETURNING id",
            (category_id,)
        )
        result = cursor.fetchone()
        return result is not None



def create_book(title, description=None, price=None, url=None, category_id=None):
    #Создание книги
    with get_cursor(commit=True) as cursor:
        cursor.execute(
            """INSERT INTO books (title, description, price, url, category_id) 
               VALUES (%s, %s, %s, %s, %s) 
               RETURNING id, title, description, price, url, category_id""",
            (title, description, price, url, category_id)
        )
        result = cursor.fetchone()
        return Book.from_dict(result) if result else None

def get_book(book_id):
    #Получение книги по ID
    with get_cursor() as cursor:
        cursor.execute(
            """SELECT b.id, b.title, b.description, b.price, b.url, b.category_id,
                      c.id as cat_id, c.title as cat_title
               FROM books b
               LEFT JOIN categories c ON b.category_id = c.id
               WHERE b.id = %s""",
            (book_id,)
        )
        result = cursor.fetchone()
        if result:
            book = Book.from_dict(result)
            if result.get('cat_id'):
                book.category = Category(id=result['cat_id'], title=result['cat_title'])
            return book
        return None

def get_all_books(limit=100, offset=0):
    #Получение всех книг с пагинацией
    with get_cursor() as cursor:
        cursor.execute(
            """SELECT b.id, b.title, b.description, b.price, b.url, b.category_id,
                      c.id as cat_id, c.title as cat_title
               FROM books b
               LEFT JOIN categories c ON b.category_id = c.id
               ORDER BY b.id
               LIMIT %s OFFSET %s""",
            (limit, offset)
        )
        results = cursor.fetchall()
        books = []
        for row in results:
            book = Book.from_dict(row)
            if row.get('cat_id'):
                book.category = Category(id=row['cat_id'], title=row['cat_title'])
            books.append(book)
        return books

def get_books_by_category(category_id):
    #Получение книг по категории
    with get_cursor() as cursor:
        cursor.execute(
            """SELECT b.id, b.title, b.description, b.price, b.url, b.category_id,
                      c.id as cat_id, c.title as cat_title
               FROM books b
               LEFT JOIN categories c ON b.category_id = c.id
               WHERE b.category_id = %s""",
            (category_id,)
        )
        results = cursor.fetchall()
        books = []
        for row in results:
            book = Book.from_dict(row)
            if row.get('cat_id'):
                book.category = Category(id=row['cat_id'], title=row['cat_title'])
            books.append(book)
        return books

def update_book(book_id, title=None, description=None, price=None, url=None, category_id=None):
    #Обновление книги
    with get_cursor(commit=True) as cursor:
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = %s")
            params.append(title)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if price is not None:
            updates.append("price = %s")
            params.append(price)
        if url is not None:
            updates.append("url = %s")
            params.append(url)
        if category_id is not None:
            updates.append("category_id = %s")
            params.append(category_id)
        
        if not updates:
            return get_book(book_id)
        
        params.append(book_id)
        query = f"""
            UPDATE books 
            SET {', '.join(updates)} 
            WHERE id = %s 
            RETURNING id, title, description, price, url, category_id
        """
        cursor.execute(query, params)
        result = cursor.fetchone()
        return Book.from_dict(result) if result else None

def delete_book(book_id):
    #Удаление книги
    with get_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM books WHERE id = %s RETURNING id",
            (book_id,)
        )
        result = cursor.fetchone()
        return result is not None

def search_books(search_term):
    #Поиск книг по названию или описанию
    with get_cursor() as cursor:
        cursor.execute(
            """SELECT b.id, b.title, b.description, b.price, b.url, b.category_id,
                      c.id as cat_id, c.title as cat_title
               FROM books b
               LEFT JOIN categories c ON b.category_id = c.id
               WHERE b.title ILIKE %s OR b.description ILIKE %s""",
            (f'%{search_term}%', f'%{search_term}%')
        )
        results = cursor.fetchall()
        books = []
        for row in results:
            book = Book.from_dict(row)
            if row.get('cat_id'):
                book.category = Category(id=row['cat_id'], title=row['cat_title'])
            books.append(book)
        return books