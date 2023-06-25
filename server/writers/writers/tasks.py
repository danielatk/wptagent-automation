import io
from writers.celery import app, logger, QUEUE

@app.task(name='writers.save_file')
@app.task(name=f'{QUEUE}.writers.save_file')
def save_file(payload):
    logger.info(payload)
