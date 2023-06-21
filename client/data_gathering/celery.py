from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab
import os
from kombu import Exchange, Queue, binding

BACKEND = os.environ.get('BACKEND', 'rpc://guest:guest@localhost/')
BROKER  = os.environ.get('BROKER', 'amqp://guest:guest@localhost/')
QUEUE   = os.environ.get('QUEUE', 'default')

logger = get_task_logger(__name__)

app = Celery('data_gathering',
            backend=BACKEND,
            broker=BROKER,
            include=['data_gathering.data_gathering.tasks'])

app.conf.task_create_missing_queues = False

exchange = Exchange('data_gathering', type='topic')
app.conf.task_queues = (
    Queue(f'data_gathering.{QUEUE}', exchange=exchange, bindings=[
        binding(exchange, routing_key=f'{QUEUE}.data_gathering.#'),
        binding(exchange, routing_key=f'data_gathering.#'),
    ]),
)


#app.conf.task_default_exchange = 'data_gathering'
#app.conf.task_default_exchange_type = 'topic'
#app.conf.task_default_routing_key = 'data_gathering.#'

#app.conf.beat_schedule = {
#    'test-task': {
#        'task': 'tasks.reload_cache',
#        'schedule': crontab(minute=0, hour='*/3'),
#        'options': {'exchange': 'broadcast_tasks'}
#    },
#}

# Optional configuration, see the application user guide.
app.conf.update(result_expires=3600)

if __name__ == '__main__':
    app.start()
