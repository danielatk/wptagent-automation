import os
import logging
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from celery import Celery
from celery.utils.log import get_task_logger
from kombu import Exchange, Queue, binding

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

BACKEND = os.environ.get('BACKEND', 'rpc://guest:guest@localhost/')
BROKER  = os.environ.get('BROKER', 'amqp://guest:guest@localhost/')
QUEUE   = os.environ.get('QUEUE', 'default')
SERVER  = os.environ.get('SERVER', 'http://0.0.0.0:1234')
IPV6    = os.environ.get('IPV6', 'false') == 'true'
APS_DB  = '/data/apscheduler.db'

logger = get_task_logger(__name__)

jobstores = {
    'default': SQLAlchemyJobStore(url=f'sqlite:///{APS_DB}')
}
executors = {
    'default': ThreadPoolExecutor(4),
    'processpool': ProcessPoolExecutor(2)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 2
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

app = Celery('data_gathering',
            backend=BACKEND,
            broker=BROKER,
            include=['data_gathering.data_gathering.tasks'])

# app.conf.task_create_missing_queues = False
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_max_retries = None # try forever

exchange = Exchange('data_gathering', type='topic')
app.conf.task_queues = (
    Queue(f'data_gathering.{QUEUE}', exchange=exchange, bindings=[
        binding(exchange, routing_key=f'{QUEUE}.data_gathering.#'),
        binding(exchange, routing_key='data_gathering.#'),
    ]),
)

# Optional configuration, see the application user guide.
app.conf.update(result_expires=3600)

if __name__ == '__main__':
    logger.info('Starting scheduler...')
    scheduler.start()
    logger.info('Scheduler started.')
    logger.info('Running celery application...')
    app.start(['-Q', f'data_gathering.{QUEUE}', '-n', QUEUE, '-l', 'info', '-E'])
    logger.info('Done.')
