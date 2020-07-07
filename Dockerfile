FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt /app

RUN apk update && \
    apk --no-cache add gcc \
    python3-dev \
    musl-dev \
    libpq

RUN pip --no-cache-dir install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python3", "run.py"]
