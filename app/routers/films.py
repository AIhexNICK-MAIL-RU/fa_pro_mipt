"""Модуль для операций с фильмами"""

from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select, delete
from sqlalchemy.exc import SQLAlchemyError
from app.db import  get_session
from app.models.models import Film as Film_db, Ratings
from app.schemas.schemas_obj import Film
from app.core.security import get_current_user



router = APIRouter(prefix="/films", tags=["Операции с фильмами"])


@router.get("/get_full_list", status_code=status.HTTP_200_OK)
def get_full_list(session: Session = Depends(get_session)) -> list[Film_db]:
    """Возвращает полный лист фильмов"""
    result = session.exec(select(Film_db)).all()
    return result


@router.post("/create_film", status_code=status.HTTP_201_CREATED)
def create_film(film: Film, session: Session = Depends(get_session),
                 _ = Depends(get_current_user)) -> Film_db:
    """Создает запись о фильме. Требуется авторизация."""
    new_film = Film_db(
        title = film.title,
        author = film.author,
        genre = film.genre
    )
    try:
        session.add(new_film)
        session.commit()
        session.refresh(new_film)
    except SQLAlchemyError as _:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Комбинация фильм-автор должна быть уникальной.") from _
    return new_film


@router.delete("/delete_track", status_code=status.HTTP_204_NO_CONTENT)
def delete_film(film_id: int, session: Session = Depends(get_session),
                 _ = Depends(get_current_user)):
    """Каскадно удаляет запись о фильме и его оценках. Требуется авторизация. """
    try:
        # удаляем все оценки фильма. Если он не существует, ошибка не возникнет!
        stmt_rating = delete(Ratings).where(Ratings.film_id == film_id)
        session.exec(stmt_rating)
        session.commit()
        # удаляем трек из таблицы фильмов. Если его нет - ошибка возникнет!
        stmt_film = select(Film_db).where(Film_db.id == film_id)
        for_delete = session.exec(stmt_film).one()
        session.delete(for_delete)
        session.commit()
    except SQLAlchemyError as _:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Фильм не существует.") from _
    return  for_delete
