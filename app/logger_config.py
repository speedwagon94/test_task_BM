import logging

def configure_logger():
    # Устанавливаем уровень логгирования (можно настроить по вашему усмотрению)
    logging.basicConfig(level=logging.INFO)

    # Создаем логгер и устанавливаем формат логов
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Создаем обработчик для записи логов в файл
    file_handler = logging.FileHandler('app/app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
