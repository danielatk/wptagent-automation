import io
from urllib.parse import urlparse
from datetime import datetime, timedelta
from scipy.stats import expon
from apscheduler.triggers.cron import CronTrigger
from data_gathering.celery import app, scheduler, logger, QUEUE, SERVER, IPV6
from .utils import *

EXPONENTIAL_MEAN_EXPERIMENTO_1_INTERVAL = 30

@app.task(name='data_gathering.send_tasks')
@app.task(name=f'{QUEUE}.data_gathering.send_tasks')
def send_tasks_to_server():
    send_results_and_delete(app, 'writers.save')
    
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

@app.task(name='data_gathering.local_schedule')
@app.task(name=f'{QUEUE}.data_gathering.local_schedule')
def local_schedule(func: str, schedule: str, kwargs: dict):
    FUNC_NAME_TO_FUNC = {
        'experimento_1': experimento_1,
        'ndt7': ndt7,
        'traceroute': traceroute,
    }
    if func not in FUNC_NAME_TO_FUNC:
        raise ValueError()
    job = scheduler.add_job(FUNC_NAME_TO_FUNC[func], CronTrigger.from_crontab(schedule), kwargs=kwargs)
    return job.id

@app.task(name=f'{QUEUE}.data_gathering.get_local_schedule')
def get_local_schedule():
    with io.StringIO() as f:
        scheduler.print_jobs(out=f)
        f.seek(0)
        return f.read()

@app.task(name='data_gathering.experimento_1')
@app.task(name=f'{QUEUE}.data_gathering.experimento_1')
def experimento_1(schedule_next: bool = False):
    """
    Ordem de execução:
        - agenda a próxima execução do experimento de acordo com ~exp(30)
        - tira na moeda entre setupNavigationFilePath e setupReproductionFilePath -> X
        - realiza o setup do teste X (obtém url)
        - traceroute
        - realiza o teste X no selenium
        - realiza o teste X no puppeteer
        - realiza o teste ndt
    """
    mac = QUEUE[4:]
    now = datetime.now().timestamp()
    result = {
        'task': 'experimento_1',
        'started': now,
        'mac': mac,
    }
    # schedule APS
    if schedule_next:
        time_in_minutes = expon.rvs(scale=int(EXPONENTIAL_MEAN_EXPERIMENTO_1_INTERVAL), size=1)[0]
        next_run = now + timedelta(minutes=time_in_minutes)
        scheduler.add_job(experimento_1, 'date', run_date=next_run, args=[True])
        logger.info(f'Next execution: {next_run}')
    # navigation or reproduction?
    experiment = get_experiment_type_at_random()
    result['experiment'] = experiment
    # setup
    url = get_url_for_experiment_type(experiment)
    use_adblock = random.random() < 0.5
    resolution_type = 1 if random.random() < 0.5 else 2
    result['url'] = url
    result['use_adblock'] = use_adblock
    result['resolution_type'] = resolution_type
    # traceroute
    domain = urlparse(url).netloc
    traceroute_result = call_traceroute(domain)
    result['traceroute'] = traceroute_result
    # browser experiments
    unlock_chrome_profile()
    result['browser'] = {}
    browser_experiments = get_browser_experiment_func(experiment)
    for method, run_func in zip(['selenium', 'puppeteer'], browser_experiments):
        result['browser'][method] = run_func(url, use_adblock, resolution_type, mac, SERVER)
    # ndt
    result['ndt'] = ndt_experiment(IPV6)
    # save and send
    save_and_send(result, app)
    return result
