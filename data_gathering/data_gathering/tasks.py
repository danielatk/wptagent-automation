from .utils import call_ndt7, call_traceroute, update_system
from data_gathering.celery import app, logger, QUEUE
import os

@app.task(name=f'data_gathering.traceroute')
@app.task(name=f'{QUEUE}.data_gathering.traceroute')
def traceroute(domain):
    output = call_traceroute(domain)
    logger.info(output)

@app.task(name=f'data_gathering.ndt7')
@app.task(name=f'{QUEUE}.data_gathering.ndt7')
def traceroute():
    output = call_ndt7()
    logger.info(output)

@app.task(name=f'{QUEUE}.data_gathering.get_version')
def get_version():
    return os.environ.get('VERSION', 'NOT SET')

@app.task(name=f'data_gathering.set_version')
@app.task(name=f'{QUEUE}.data_gathering.set_version')
def set_version(new_version):
    update_system(new_version)
