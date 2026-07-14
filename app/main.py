from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import categories, books
from app.db.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Library API", lifespan=lifespan)

app.include_router(categories.router)
app.include_router(books.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
