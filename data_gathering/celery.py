from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab

QUEUE = 'teste'

logger = get_task_logger(__name__)

app = Celery('data_gathering',
            backend='rpc://quest@localhost//',
            broker='pyamqp://guest@localhost//',
            include=['data_gathering.data_gathering.tasks'])

app.conf.task_routes = {f'data_gathering.{QUEUE}.*': {'queue': QUEUE, 'type': 'topic', 'exchange': 'data_gathering'}}

app.conf.beat_schedule = {
    'test-task': {
        'task': 'tasks.reload_cache',
        'schedule': crontab(minute=0, hour='*/3'),
        'options': {'exchange': 'broadcast_tasks'}
    },
}

# Optional configuration, see the application user guide.
app.conf.update(result_expires=3600)

if __name__ == '__main__':
    app.start()
