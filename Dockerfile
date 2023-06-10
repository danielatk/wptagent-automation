FROM python:3.9.13

ENV QUEUE="default"

WORKDIR /app
COPY . /app/data_gathering

RUN pip install -r data_gathering/requirements.txt

CMD ["sh", "-c", "celery -A data_gathering worker -Q data_gathering.${QUEUE} -n ${QUEUE} -l info"]
#CMD ["sh", "-c", "celery -A data_gathering worker"]
