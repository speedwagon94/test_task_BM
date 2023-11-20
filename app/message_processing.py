import os
import json
import asyncio

from datetime import datetime
from aio_pika import connect, Message, DeliveryMode
from dotenv import load_dotenv

from logger_config import configure_logger
from models import Result, Item


load_dotenv()

# Загрузка переменных окружения из файла .env
BROKER_URL = f"pyamqp://{os.getenv('RABBITMQ_DEFAULT_USER')}:{os.getenv('RABBITMQ_DEFAULT_PASS')}@localhost:5672"
BROKER_URL =  os.getenv('BROKER_URL')
# Конфигурация логгера
logger = configure_logger()

async def process_message(message, db_session):
    # Обработка сообщения из очереди
    try:
        item = Item.parse_raw(message.body)
        cyrillic_x_count = item.text.lower().count("х")
        datetime_obj = datetime.strptime(item.datetime, "%d.%m.%Y %H:%M:%S.%f")
        result = Result(
            title=item.title,
            x_avg_count_in_line=cyrillic_x_count,
            datetime=datetime_obj
        )
        with db_session() as session:
            session.add(result)
            session.commit()
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
async def consume_messages(connection, db_session):
    # Потребление сообщений из очереди
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("text_queue")
        async def callback(message):
            try:
                await process_message(message, db_session)
            except Exception as e:
                logger.error(f"Ошибка в callback: {e}")
            finally:
                await message.ack()
        await queue.consume(callback)
async def publish_message(item: Item):
    # Публикация сообщения в очередь
    try:
        connection = await connect(BROKER_URL)
        async with connection:
            channel = await connection.channel()
            message_body = json.dumps(item.dict())
            message = Message(message_body.encode(), delivery_mode=DeliveryMode.PERSISTENT)
            await channel.default_exchange.publish(message, routing_key="text_queue")
    except Exception as e:
        logger.error(f"Ошибка при публикации сообщения: {e}")
async def consume_messages_background(connection, db_session):
    # Асинхронный фоновый процесс потребления сообщений
    while True:
        try:
            if not connection or connection.is_closed:
                connection = await connect(BROKER_URL)
            await consume_messages(connection, db_session)
        except Exception as e:
            logger.error(f"Ошибка в consume_messages_background: {e}")
            await asyncio.sleep(1)
