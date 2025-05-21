FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN chmod +x /app/entrypoint.sh

CMD ["./entrypoint.sh"]