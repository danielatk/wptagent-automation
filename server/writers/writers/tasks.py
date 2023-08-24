import json

from writers.celery import app, logger, QUEUE

SAVE_DIR = '/data'

def save_reproduction_file(payload):
    browser = payload['browser']
    if 'reproduction' not in browser:
        return
    device = payload['mac'].replace(':', '')
    reproduction = browser['reproduction']
    time = int(reproduction['started'])
    filename = f"{reproduction['video_id']}_{device}_{time}_sfn.json"
    with open(f'{SAVE_DIR}/{filename}', 'w') as f:
            f.writelines([json.dumps(line) for line in reproduction['data']])

def save_navigation_files(payload):
    browser = payload['browser']
    if 'navigation' not in browser:
        return
    navigation = browser['navigation']
    device = payload['mac'].replace(':', '')
    for url in navigation.keys():
        time = navigation[url]['started']
        parsed_url = url.replace("http://", "").replace("https://", "")
        filename = f'{parsed_url}_{device}_{time}_plugin.json'
        with open(f'{SAVE_DIR}/{filename}', 'w') as f:
            f.writelines([json.dumps(line) for line in navigation[url]['data']])

def save_ndt_file(payload):
    ndt = payload['ndt']
    device = payload['mac'].replace(':', '')
    time = int(payload['started'])
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
    save_reproduction_file(payload)
    save_navigation_files(payload)
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