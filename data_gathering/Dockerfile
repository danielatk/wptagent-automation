FROM python:3.9.13

WORKDIR /app
COPY . /app/data_gathering

RUN pip install -r data_gathering/requirements.txt

CMD ["celery", "-A", "data_gathering", "worker", "-Q", "teste"]
