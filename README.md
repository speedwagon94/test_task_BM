# Запуск:

# 1. Клонирование репозитория
git clone https://github.com/speedwagon94/test_task_BM.git

# 2. Создание и активация виртуального окружения
python -m venv venv
# Для Windows:
.\venv\Scripts\activate
# Для Unix-подобных систем:
source venv/bin/activate

# 3. Добавьте ключи в файл .env


# 5. Сборка Docker-образа
docker build -t x_avg_count .

# 6. Сборка Docker-контейнера с использованием Docker Compose
docker-compose build
