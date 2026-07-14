# Library API

Небольшой API для работы с книгами и категориями. Приложение написано на FastAPI, для хранения данных используется PostgreSQL, для работы с базой — SQLAlchemy.

## Подготовка проекта

Команды нужно выполнять из корня проекта в WSL.

Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка базы данных

Приложение читает настройки PostgreSQL из файла `.env`. Пример содержимого файла:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=octagon
DB_USER=octagon
DB_PASSWORD=12345
```

База данных и пользователь PostgreSQL должны быть созданы заранее. Таблицы создаются автоматически при запуске приложения.

Если нужно заполнить базу тестовыми категориями и книгами, выполните:

```bash
python -m app.init_db
```

## Запуск

```bash
uvicorn app.main:app --reload
```

После запуска API будет доступен по адресу `http://127.0.0.1:8000`.

Swagger: `http://127.0.0.1:8000/docs`

ReDoc: `http://127.0.0.1:8000/redoc`

Проверить работу сервиса можно командой:

```bash
curl -i http://127.0.0.1:8000/health
```

## Эндпоинты

### Категории

`GET /categories/` — получить список категорий.

`GET /categories/{category_id}` — получить категорию по идентификатору.

`POST /categories/` — создать категорию.

`PUT /categories/{category_id}` — изменить категорию.

`DELETE /categories/{category_id}` — удалить категорию.

### Книги

`GET /books/` — получить список книг.

`GET /books/?category_id=1` — получить книги указанной категории.

`GET /books/{book_id}` — получить книгу по идентификатору.

`POST /books/` — создать книгу.

`PUT /books/{book_id}` — изменить книгу.

`DELETE /books/{book_id}` — удалить книгу.

При создании или изменении книги приложение проверяет, существует ли указанная категория.

## Примеры работы

Скриншоты Swagger, запроса к API и данных в PostgreSQL находятся в папке `examples`.
