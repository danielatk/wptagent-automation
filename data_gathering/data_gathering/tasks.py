from .utils import call_ndt7, call_traceroute
from data_gathering.celery import app, logger, QUEUE

@app.task(name=f'data_gathering.traceroute')
@app.task(name=f'{QUEUE}.data_gathering.traceroute')
def traceroute():
    output = call_traceroute('google.com')
    logger.info(output)

@app.task(name=f'data_gathering.ndt7')
@app.task(name=f'{QUEUE}.data_gathering.ndt7')
def traceroute():
    output = call_ndt7()
    logger.info(output)

