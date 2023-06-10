from data_gathering.celery import app, logger, QUEUE

@app.task(name=f'data_gathering.add')
@app.task(name=f'{QUEUE}.data_gathering.add')
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    print('FOI CHAMADO!!!')
    return x + y

