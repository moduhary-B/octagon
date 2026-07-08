import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.crud import get_all_categories, get_all_books, get_books_by_category

def main():
    print("=" * 60)
    print("БИБЛИОТЕКА КНИГ")
    print("=" * 60)
    
    categories = get_all_categories()
    print(f"\nВсего категорий: {len(categories)}")
    
    for category in categories:
        print(f"\nКатегория: {category.title}")
        print("-" * 40)
        
        books = get_books_by_category(category.id)
        
        if books:
            for i, book in enumerate(books, 1):
                print(f"  {i}. {book.title}")
                if book.description:
                    print(f"     Описание: {book.description}")
                if book.price:
                    print(f"     Цена: {book.price} руб.")
                print()
        else:
            print("  (нет книг в этой категории)")
    
    print("\n" + "=" * 60)
    print("ВСЕ КНИГИ В БАЗЕ ДАННЫХ:")
    print("=" * 60)
    
    all_books = get_all_books()
    for i, book in enumerate(all_books, 1):
        category_title = book.category.title if book.category else "Без категории"
        print(f"{i}. {book.title}")
        print(f"   Категория: {category_title}")
        if book.price:
            print(f"   Цена: {book.price} руб.")
        print()

if __name__ == "__main__":
    main()