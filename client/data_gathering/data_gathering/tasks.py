from data_gathering.celery import app, logger, QUEUE
from .utils import call_ndt7, call_traceroute, get_runtime_version

@app.task(name='data_gathering.traceroute')
@app.task(name=f'{QUEUE}.data_gathering.traceroute')
def traceroute(domain):
    output = call_traceroute(domain)
    logger.info(output)

@app.task(name='data_gathering.ndt7')
@app.task(name=f'{QUEUE}.data_gathering.ndt7')
def ndt7():
    output = call_ndt7()
    logger.info(output)


@app.task(name=f'{QUEUE}.data_gathering.get_version')
def get_version():
    return get_runtime_version()

@app.task(name='data_gathering.get_queue')
def get_queue():
    return QUEUE
