FROM python:3.11-alpine

WORKDIR /app/

COPY requirements.txt /app/

RUN apk update && \
    apk add --no-cache py3-pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python","./main.py"]
