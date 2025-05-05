"""Модуль  аутентификации"""
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from app.models.models import User
from app.config import settings as cnf
from app.db import get_session



SECRET_KEY = cnf.secret_key
ALGORITHM = cnf.algo
ACCESS_TOKEN_EXPIRE_MINUTES = cnf.access_token_expire_minutes



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def hash_password(password: str) -> str:
    """Хэширование пароля"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Создание токена"""
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    """Расшифровка токена"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), session = Depends(get_session)) -> User:
    """Текущий пользователь"""
    login = decode_token(token)
    if not login:
        raise HTTPException(status_code=401, detail="Невалидный токен")
    user = session.exec(select(User).where(User.login == login)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
