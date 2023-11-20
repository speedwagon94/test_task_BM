import uvicorn

import asyncio

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import func
from aio_pika import connect

from logger_config import configure_logger
from models import Result, Item
from db import SessionLocal
from message_processing import BROKER_URL, consume_messages_background, publish_message


# Конфигурация логгера
logger = configure_logger()

def create_app():
    app = FastAPI(docs_url='/')


    @app.on_event("startup")
    async def startup_event():
        # Событие при старте приложения
        try:
            connection = await connect(BROKER_URL)
            asyncio.create_task(consume_messages_background(connection, SessionLocal))
        except Exception as e:
            logger.error(f"Ошибка при старте: {e}")

    @app.post("/upload")
    async def upload_data(item: Item):
        # Обработчик POST-запроса для загрузки данных
        try:
            await publish_message(item)
            await asyncio.sleep(3)
            return {"message": "Данные успешно загружены"}
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            return JSONResponse(content={"error": "Внутренняя ошибка сервера"}, status_code=500)

    @app.get("/calculate")
    async def calculate_average():
        # Обработчик GET-запроса для вычисления среднего значения
        try:
            response_data = []

            with SessionLocal() as db_session:
                results = (
                    db_session.query(
                        Result.datetime,
                        Result.title,
                        func.coalesce(func.avg(Result.x_avg_count_in_line), 0).label("avg_x_count_in_line")
                    )
                    .group_by(Result.datetime, Result.title)
                    .all()
                )

                for result in results:
                    response_data.append({
                        "datetime": result.datetime.strftime("%d.%m.%Y %H:%M:%S.%f")[:-3],
                        "title": result.title,
                        "x_avg_count_in_line": float(result.avg_x_count_in_line)
                    })

            return JSONResponse(content=response_data)
        except Exception as e:
            logger.error(f"Ошибка при вычислении среднего значения: {e}")
            return JSONResponse(content={"error": "Внутренняя ошибка сервера"}, status_code=500)

    return app

def main():
    # Запуск приложения
    uvicorn.run(
        "app:create_app",
        host='127.0.0.1', port=8000,
        reload=True,
    )

if __name__ == '__main__':
    main()
