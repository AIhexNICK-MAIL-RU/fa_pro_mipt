"""Инициализация базы"""
from sqlmodel import create_engine, Session, SQLModel
from app.config import settings as cnf


DB_URL = (
        f"postgresql://{cnf.db_username}:{cnf.db_password}@{cnf.db_host}"
        f":{cnf.db_port}/{cnf.db_name}"
)

engine = create_engine(DB_URL, echo=True)

def get_session():
    """Объект сессии"""
    with Session(engine) as session:
        yield session

# для создания базы, вызывается из мэйна.
def init_database():
    """Создает таблицы"""
    SQLModel.metadata.create_all(engine)
