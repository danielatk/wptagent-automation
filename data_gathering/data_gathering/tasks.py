from data_gathering.celery import app, logger, QUEUE

@app.task(name=f'data_gathering.{QUEUE}.add')
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y

