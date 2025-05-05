"""Модуль для операций с оценками (рейтингом)"""
from typing import List, Callable
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select, func, and_
from app.db import get_session
from app.core.security import get_current_user
from app.schemas.schemas_obj import Ratings
from app.models.models import Ratings as Rating_db, Film

func: Callable # нужно только для pylint

router = APIRouter(prefix="/ratings", tags=["Операции с оценками"])

@router.patch("/set_rating", status_code=status.HTTP_201_CREATED)
def set_rating(rating: Ratings, login=Depends(get_current_user),
               session=Depends(get_session)) -> Rating_db:
    """Устанавливает оценку фильма, требуется логин юзера"""

    stmt = select(Film).where(Film.id == rating.film_id)
    check = session.exec(stmt).all()
    if check == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фильма не существует."
            )
    new_rating = Rating_db(
        user_id = login.id,
        film_id = rating.film_id,
        estimate = rating.estimate
    )
    try:
        session.add(new_rating)
        session.commit()
        session.refresh(new_rating)
    except SQLAlchemyError as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Оценка уже существует. Для изменения оценки воспользуйтесь /change_rating."
            ) from _
    return new_rating



@router.patch("/change_rating", status_code=status.HTTP_201_CREATED)
def change_rating(rating: Ratings, login=Depends(get_current_user),
                  session=Depends(get_session)) -> Rating_db:
    """Меняет оценку фильма, требуется логин юзера"""

    stmt = select(Rating_db).where(and_(
        Rating_db.user_id == login.id,
        Rating_db.film_id == rating.film_id))
    try:
        new_rating = session.scalars(stmt).one()
        new_rating.estimate = rating.estimate
        session.commit()
        session.refresh(new_rating)
    except SQLAlchemyError as _:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Оценки не существует. Для создания оценки воспользуйтесь /set_rating."
            ) from _
    return new_rating

@router.get("/get_my_recommendations", status_code=status.HTTP_200_OK)
def get_my_recommend(user_id: int, session: Session = Depends(get_session)) -> List[Film]:
    """Возвращает список рекомендованных фильмов для указанного юзера"""
    # кол-во предпочитаемых жанров. Чем больше, тем хаотичнее выборка, чем меньше, тем тривиальнее
    genre_limit = 2
    # Получаем любимые жанры юзера
    stmt = (
        select(Film.genre)
        .join(Rating_db, Rating_db.film_id == Film.id)
        .where(and_(
            Rating_db.user_id == user_id,
            Rating_db.estimate >= 4
        ))
        .group_by(Film.genre)
        .order_by(func.count().desc())
        .limit(genre_limit)
    )
    user_genres = list(session.exec(stmt).all())

    if not user_genres:
        return []

    #  Находим похожих юзеров(высоко оценили фильмы этих жанров)
    stmt = (
        select(Rating_db.user_id)
        .join(Film, Film.id == Rating_db.film_id)
        .where(and_(
        Rating_db.user_id != user_id,
            Rating_db.estimate >= 4,
            Film.genre.in_(user_genres)
        ))
        .group_by(Rating_db.user_id)
        .having(func.count() >= 2)
    )
    similar_users = list(session.exec(stmt).all())

    if not similar_users:
        return []

    # Получаем фильмы, которые высоко оценили похожие юзеры
    stmt = (select(Film).join(Rating_db, Rating_db.film_id == Film.id).where(
        and_(Rating_db.user_id.in_(similar_users), # pylint: disable=no-member
             Rating_db.estimate >= 4)).group_by(
            Film.id))

    # Находим фильмы, которые юзер уже оценил
    rated_films =list(session.exec(
        select(Rating_db.film_id)
        .where(Rating_db.user_id == user_id)
    ).all())

    # Исключаем оцененные треки
    if rated_films:
        stmt = stmt.where(Film.id.not_in(rated_films)) # pylint: disable=no-member

    # Сортируем и ограничиваем результат
    stmt = (
        stmt.order_by(
            func.count().desc(),
            func.avg(Rating_db.estimate).desc()
        )
        .limit(3)
    )
    return session.exec(stmt).all()
