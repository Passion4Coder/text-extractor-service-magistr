FROM python:3.12-slim

RUN apt-get update && apt-get install -y antiword

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade "pip<24.1"
RUN pip install --no-cache-dir -r requirements.txt --no-dependencies

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]