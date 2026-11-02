from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройки подключения (укажите свои login, password и имя базы данных)
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/notes_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Создание и закрытие сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
