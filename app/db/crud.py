from sqlalchemy.orm import Session, joinedload

from app.db.models import Book, Category


def create_category(db: Session, title: str):
    category = Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_title(db: Session, title: str):
    return db.query(Category).filter(Category.title == title).first()


def get_all_categories(db: Session):
    return db.query(Category).order_by(Category.title).all()


def update_category(db: Session, category_id: int, title: str):
    category = get_category(db, category_id)
    if category:
        category.title = title
        db.commit()
        db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if not category:
        return False
    db.query(Book).filter(Book.category_id == category_id).update(
        {Book.category_id: None}
    )
    db.delete(category)
    db.commit()
    return True


def create_book(
    db: Session,
    title: str,
    description=None,
    price=None,
    url=None,
    category_id=None,
):
    book = Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int):
    return (
        db.query(Book)
        .options(joinedload(Book.category))
        .filter(Book.id == book_id)
        .first()
    )


def get_all_books(db: Session, limit=100, offset=0):
    return (
        db.query(Book)
        .options(joinedload(Book.category))
        .order_by(Book.id)
        .limit(limit)
        .offset(offset)
        .all()
    )


def get_books_by_category(db: Session, category_id: int):
    return (
        db.query(Book)
        .options(joinedload(Book.category))
        .filter(Book.category_id == category_id)
        .all()
    )


def update_book(
    db: Session,
    book_id: int,
    title=None,
    description=None,
    price=None,
    url=None,
    category_id=None,
):
    book = get_book(db, book_id)
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
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True


def search_books(db: Session, search_term: str):
    return (
        db.query(Book)
        .options(joinedload(Book.category))
        .filter(
            Book.title.ilike(f"%{search_term}%")
            | Book.description.ilike(f"%{search_term}%")
        )
        .all()
    )
