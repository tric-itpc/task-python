FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y


WORKDIR /app
COPY . /app/app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8099", "--workers", "1"]