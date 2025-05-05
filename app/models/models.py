"""Описание структуры таблиц"""

from sqlmodel import SQLModel, Field as SQLField, UniqueConstraint


class Film(SQLModel, table=True):
    """Модель фильмов для базы"""
    __table_args__ = (
        UniqueConstraint('title', 'author', name='film_and_author_constraint'),
    )
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    title: str
    author: str
    genre: str

class User(SQLModel, table=True):
    """Модель пользователя для базы"""
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    login: str = SQLField(unique=True)
    first_name: str = SQLField(default=None, nullable=True)
    last_name: str = SQLField(default=None, nullable=True)
    email: str = SQLField(default=None, nullable=True)
    hashed_password: str

class Ratings(SQLModel, table=True):
    """Модель рейтинга для базы"""
    __table_args__ = (
        UniqueConstraint('user_id', 'film_id', name='user_and_film_constraint'),
    )

    id: int = SQLField(default=None, nullable=False, primary_key=True)
    user_id: int = SQLField(default=None, nullable=False, foreign_key="user.id")
    film_id: int = SQLField(default=None, nullable=False, foreign_key="film.id")
    estimate: int = SQLField(ge=1, le=5)
