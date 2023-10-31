FROM python:3.10-slim

LABEL owner="github.com/advatroniks"

ENV PYTHONPATH=${PYTHONPATH}:/home/app/score_spin

WORKDIR /home/app/score_spin

COPY requirements.txt /home/app/score_spin

RUN pip install -r requirements.txt

COPY ../.. .

EXPOSE 80

#RUN sh -c 'alembic upgrade head'

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]

