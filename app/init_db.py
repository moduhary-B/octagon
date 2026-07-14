import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session

from app.db.db import SessionLocal, init_db
from app.db.crud import create_category, create_book, get_all_categories


def init_data():
    with SessionLocal() as db:
        _init_data(db)


def _init_data(db: Session):
    existing_categories = get_all_categories(db)
    
    if existing_categories:
        print(f"База данных уже заполнена! Найдено категорий: {len(existing_categories)}")
        print("Пропускаем создание дубликатов.")
        return
    
    cat1 = create_category(db, "Фантастика")
    cat2 = create_category(db, "Детектив")
    
    print(f"Созданы категории: {cat1.title}, {cat2.title}")
    
    books_fantasy = [
        {"title": "1984", "description": "Роман-антиутопия", "price": 450.00},
        {"title": "Дюна", "description": "Эпическая сага", "price": 650.00},
        {"title": "Сталкер", "description": "Пикник на обочине", "price": 380.00},
        {"title": "Колыбель для кошки", "description": "Сатирическая фантастика", "price": 420.00}
    ]
    
    for book_data in books_fantasy:
        create_book(
            db,
            title=book_data["title"],
            description=book_data["description"],
            price=book_data["price"],
            category_id=cat1.id
        )
        print(f"Добавлена книга: {book_data['title']}")
    
    books_detective = [
        {"title": "Собака Баскервилей", "description": "Дело Холмса", "price": 390.00},
        {"title": "Убийство в Восточном экспрессе", "description": "Детектив", "price": 420.00},
        {"title": "Девушка с татуировкой дракона", "description": "Скандинавский триллер", "price": 510.00}
    ]
    
    for book_data in books_detective:
        create_book(
            db,
            title=book_data["title"],
            description=book_data["description"],
            price=book_data["price"],
            category_id=cat2.id
        )
        print(f"Добавлена книга: {book_data['title']}")

if __name__ == "__main__":
    print("Создание таблиц...")
    init_db()
    print("Начинаем заполнение базы данных...")
    init_data()
    print("База данных успешно заполнена!")
