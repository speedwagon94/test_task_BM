import os

from sqlalchemy import create_engine
import sqlalchemy.orm

from dotenv import load_dotenv

from models import Base


load_dotenv()

# Загрузка переменных окружения из файла .env
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)