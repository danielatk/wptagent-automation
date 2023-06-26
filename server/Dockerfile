FROM python:3.9.13
ENV QUEUE="default"
WORKDIR /app
RUN useradd -ms /bin/bash data_gathering_server
COPY . /app
RUN mkdir /data
RUN chown -R data_gathering:data_gathering /app /data
USER data_gathering_server
ENV PATH="$PATH:/home/data_gathering_server/.local/bin"
RUN pip install -U -r requirements.txt
CMD ["sh", "-c", "celery -A writers worker -Q writers.${QUEUE} -n ${QUEUE} -l info -E"]
