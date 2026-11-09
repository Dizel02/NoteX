from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройки для домашнего MySQL сервера (XAMPP)
MYSQL_URL = "mysql+pymysql://root:@localhost:3306"
MYSQL_DB_URL = "mysql+pymysql://root:@localhost:3306/notes_db"

try:
    # 1. Пробуем подключиться к MySQL и создать БД notes_db, если её нет
    check_engine = create_engine(MYSQL_URL, connect_args={"connect_timeout": 2})
    with check_engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS notes_db"))
        conn.commit()
    
    # Если сервер MySQL запущен — работаем на нём
    engine = create_engine(MYSQL_DB_URL, pool_pre_ping=True)
    db_type = "MYSQL"

except Exception:
    # 2. Если MySQL выключен или его нет — автоматически переключаемся на SQLite
    engine = create_engine("sqlite:///./notes.db", connect_args={"check_same_thread": False})
    db_type = "SQLITE"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
