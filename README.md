Запуск:

1. Клонируйте репозиторий: git clone https://github.com/speedwagon94/test_task_BM.git

2. Создайте и активируйте виртуальное окружение

3. Установите зависимости:

    pip install -r requirements.txt

4. Добавьте ключи в файл .env

5. Соберите Docker-образ:

    docker build -t x_avg_count .

    docker-compose build

6. Запустите Docker-контейнер:
    
    docker run -p 8000:8000 x_avg_count

    docker-compose up

