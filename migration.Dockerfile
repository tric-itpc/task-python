FROM python:3.10-slim

WORKDIR /migrations

RUN pip install psycopg2-binary

RUN pip install python-dotenv

RUN pip install alembic

RUN pip install asyncpg

COPY ../.. .

CMD ["alembic","upgrade","head"]