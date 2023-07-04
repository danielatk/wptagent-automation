import json

from writers.celery import app, logger, QUEUE

SAVE_DIR = '/data'

def save_ndt_file(payload):
    ndt = payload['ndt']
    device = payload['mac'].replace(':', '')
    time = int(payload['started'].timestamp())
    base = f'{device}_{time}_{ndt["uf"]}'
    with open(f'{SAVE_DIR}/{base}_ndt.json', 'w') as f:
        f.writelines([json.dumps(n) for n in ndt['ndt']])
    with open(f'{SAVE_DIR}/{base}_traceroute4', 'w') as f:
        f.write(ndt['traceroute-4'])
    if 'traceroute-6' in ndt:
        with open(f'{SAVE_DIR}/{base}_traceroute6', 'w') as f:
            f.write(ndt['traceroute-6'])

@app.task(name='writers.save_file')
def save_file(payload):
    logger.info(payload)
    # save traceroute
    # save browser
    # save ndt
    save_ndt_file(payload)

@app.task(name='writers.get_worker_results')
def get_results(device = None):
    task = 'data_gathering.send_tasks'
    if device:
        task = f'{device}.{task}'
    app.send_task(task, routing_key=task, exchange='data_gathering')

@app.task(name='writers.save')
@app.task(name=f'{QUEUE}.writers.save')
def save(payload):
    save_file(payload)