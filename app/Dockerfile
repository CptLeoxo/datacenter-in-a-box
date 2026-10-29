# Alpine image is enough
FROM python:3.11-slim AS tester
WORKDIR /app

COPY requirements.txt .
RUN apk add --no-cahce postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pytest -v



FROM python:3.11-slim AS runnner
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
