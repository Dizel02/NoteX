from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Подключаемся сначала к самому серверу MySQL (без указания конкретной БД)
SERVER_URL = "mysql+pymysql://root:@localhost:3306"
init_engine = create_engine(SERVER_URL, pool_pre_ping=True)

# 2. Автоматически создаем базу данных notes_db, если её нет
with init_engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS notes_db"))
    conn.commit()

# 3. Теперь спокойно настраиваем основное подключение к нашей базе
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/notes_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
