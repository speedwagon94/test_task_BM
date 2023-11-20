FROM python:3.11.0

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000"]
