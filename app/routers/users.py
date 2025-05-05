"""Модуль для операций с пользователями"""
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import  select
from app.db import  get_session
from app.models.models import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.schemas_obj import Token, User as User_sh

router = APIRouter(prefix="/users", tags=["Операции с пользователями"])

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
# def create_user(login: str, password: str, session = Depends(get_session)):
def create_user(user: User_sh, session = Depends(get_session)) -> dict:
    """Создает нового пользователя"""
    user_exists = session.exec(select(User).where(User.login == user.login)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    user_new = User(login=user.login,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    hashed_password=hash_password(user.password))
    session.add(user_new)
    session.commit()
    return {"message": "Пользователь зарегистрирован"}

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session = Depends(get_session)) -> dict:
    """Аутентифицирует пользователя, возвращает токен"""
    user = session.exec(select(User).where(User.login == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}
