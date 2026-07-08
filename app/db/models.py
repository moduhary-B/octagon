class Category:
    """Модель категории"""
    def __init__(self, id=None, title=None):
        self.id = id
        self.title = title
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title
        }
    
    @staticmethod
    def from_dict(data):
        return Category(
            id=data.get('id'),
            title=data.get('title')
        )

class Book:
    """Модель книги"""
    def __init__(self, id=None, title=None, description=None, 
                 price=None, url=None, category_id=None, category=None):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.url = url
        self.category_id = category_id
        self.category = category
    
    def to_dict(self):
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': float(self.price) if self.price else None,
            'url': self.url,
            'category_id': self.category_id
        }
        if self.category:
            result['category'] = self.category.to_dict() if isinstance(self.category, Category) else self.category
        return result
    
    @staticmethod
    def from_dict(data):
        book = Book(
            id=data.get('id'),
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price'),
            url=data.get('url'),
            category_id=data.get('category_id')
        )
        if 'category' in data and data['category']:
            if isinstance(data['category'], dict):
                book.category = Category.from_dict(data['category'])
            else:
                book.category = data['category']
        return book