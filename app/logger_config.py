import logging
import os

def configure_logger():

    logs_folder = 'logs'

    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    # Устанавливаем уровень логгирования (можно настроить по вашему усмотрению)
    logging.basicConfig(level=logging.INFO)

    # Создаем логгер и устанавливаем формат логов
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Создаем обработчик для записи логов в файл
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
