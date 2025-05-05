"""Модели для ФастАПИ(не для базы!)"""
import re
from pydantic import BaseModel, Field, EmailStr, field_validator



class Film(BaseModel):
    """Фильм для веб-интерфейса"""
    title: str = Field(max_length=80)
    author: str = Field(max_length=100)
    genre: str = None


class User(BaseModel):
    """Пользователь для веб-интерфейса"""
    login: str = Field()
    password: str
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = Field(default=None)

    @field_validator('login')
    def validate_login(cls, value): # pylint: disable=no-self-argument
        """Проверка логина"""
        if not value.strip():
            raise ValueError("Логин не может быть пустым")
        if ' ' in value:
            raise ValueError("Логин не должен содержать пробелов")
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise ValueError("Логин может содержать только буквы, цифры, '_' и '-'")
        return value


class Ratings(BaseModel):
    """Оценка трека для веб-интерфейса"""
    #hash: str
    film_id: int
    estimate: int = Field(ge=1, le=5)


class Token(BaseModel):
    """Токен для веб-интерфейса"""
    access_token: str
    token_type: str
