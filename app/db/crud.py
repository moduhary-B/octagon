from sqlalchemy.orm import joinedload
from app.db.db import get_session
from app.db.models import Category, Book


def create_category(title):
    session = get_session()
    try:
        cat = Category(title=title)
        session.add(cat)
        session.commit()
        session.refresh(cat)
        return cat
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_category(category_id):
    session = get_session()
    try:
        return session.query(Category).filter(Category.id == category_id).first()
    finally:
        session.close()


def get_category_by_title(title):
    session = get_session()
    try:
        return session.query(Category).filter(Category.title == title).first()
    finally:
        session.close()


def get_all_categories():
    session = get_session()
    try:
        return session.query(Category).order_by(Category.title).all()
    finally:
        session.close()


def update_category(category_id, title):
    session = get_session()
    try:
        cat = session.query(Category).filter(Category.id == category_id).first()
        if cat:
            cat.title = title
            session.commit()
            session.refresh(cat)
        return cat
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_category(category_id):
    session = get_session()
    try:
        cat = session.query(Category).filter(Category.id == category_id).first()
        if not cat:
            return False
        session.query(Book).filter(Book.category_id == category_id).update(
            {Book.category_id: None}
        )
        session.delete(cat)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()



def create_book(title, description=None, price=None, url=None, category_id=None):
    session = get_session()
    try:
        book = Book(
            title=title,
            description=description,
            price=price,
            url=url,
            category_id=category_id,
        )
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_book(book_id):
    session = get_session()
    try:
        return session.query(Book).options(joinedload(Book.category)).filter(Book.id == book_id).first()
    finally:
        session.close()


def get_all_books(limit=100, offset=0):
    session = get_session()
    try:
        return (
            session.query(Book)
            .options(joinedload(Book.category))
            .order_by(Book.id)
            .limit(limit)
            .offset(offset)
            .all()
        )
    finally:
        session.close()


def get_books_by_category(category_id):
    session = get_session()
    try:
        return (
            session.query(Book)
            .options(joinedload(Book.category))
            .filter(Book.category_id == category_id)
            .all()
        )
    finally:
        session.close()


def update_book(book_id, title=None, description=None, price=None, url=None, category_id=None):
    session = get_session()
    try:
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            return None
        if title is not None:
            book.title = title
        if description is not None:
            book.description = description
        if price is not None:
            book.price = price
        if url is not None:
            book.url = url
        if category_id is not None:
            book.category_id = category_id
        session.commit()
        session.refresh(book)
        return book
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_book(book_id):
    session = get_session()
    try:
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            return False
        session.delete(book)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def search_books(search_term):
    session = get_session()
    try:
        return (
            session.query(Book)
            .options(joinedload(Book.category))
            .filter(
                Book.title.ilike(f"%{search_term}%")
                | Book.description.ilike(f"%{search_term}%")
            )
            .all()
        )
    finally:
        session.close()
