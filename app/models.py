from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Float
import sqlalchemy.orm


Base = sqlalchemy.orm.declarative_base()

class Item(BaseModel):
    # Модель для данных, получаемых от клиента
    datetime: str
    title: str
    text: str

class Result(Base):
    # ORM-модель для таблицы "results" в базе данных
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime)
    title = Column(String, index=True)
    x_avg_count_in_line = Column(Float)
