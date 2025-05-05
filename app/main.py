"""Главный модуль"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from app.routers import films, users, ratings
from .db import init_database


@asynccontextmanager
async def lifespan(application: FastAPI): # pylint: disable=unused-argument
    """Асинхронный контекст-менеджер"""
    init_database()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Сервис рекомендаций фильмов",
    description="Учебный проект для сбора статистики предпочтений фильмов на "
                "фреймворке FastAPI.",
    version="0.0.1",
    contact={
        "name": "Иван",
        "url": "https://fake.url",
        "email": "sample@sample.url",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)



@app.get("/", status_code=status.HTTP_200_OK, tags=["Главная страница"])
def root() -> dict:
    """Заглавная страница"""
    return {"Для информации":"перейдите на http://127.0.0.1:80/docs"}


app.include_router(films.router)
app.include_router(users.router)
app.include_router(ratings.router)
