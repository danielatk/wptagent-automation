import os
from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from kombu import Exchange, Queue, binding

BACKEND = os.environ.get('BACKEND', 'rpc://guest:guest@localhost/')
BROKER  = os.environ.get('BROKER', 'amqp://guest:guest@localhost/')
QUEUE   = os.environ.get('QUEUE', 'default')

logger = get_task_logger(__name__)

app = Celery('data_gathering',
            backend=BACKEND,
            broker=BROKER,
            include=['writers.writers.tasks'])

app.conf.task_create_missing_queues = False
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_max_retries = None # try forever

exchange = Exchange('data_gathering', type='topic')
app.conf.task_queues = (
    Queue(f'writers.{QUEUE}', exchange=exchange, bindings=[
        binding(exchange, routing_key=f'{QUEUE}.writers.#'),
        binding(exchange, routing_key='writers.#'),
    ]),
)

app.conf.beat_schedule = {
    'get-results-from-devices': {
        'task': 'writers.get_worker_results',
        'schedule': crontab(minute='*/30'),
    },
}
app.conf.timezone = 'UTC'

# Optional configuration, see the application user guide.
app.conf.update(result_expires=3600)

if __name__ == '__main__':
    app.start()
