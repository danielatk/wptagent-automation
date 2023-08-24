import io
from datetime import datetime, timedelta
from scipy.stats import expon
from apscheduler.triggers.cron import CronTrigger
from ..model import get_number_of_pages_from_file
from ..celery import app, scheduler, logger, QUEUE, IPV6
from .utils import *
from .navigation import selenium_reproduction
import schedule

EXPONENTIAL_MEAN_EXPERIMENTO_1_INTERVAL = 30
PAGES_FILE_PATH = '/app/resources/navigation_list.csv'

@app.task(name='data_gathering.experimento_1')
@app.task(name=f'{QUEUE}.data_gathering.experimento_1')
def experimento_1(schedule_next: bool = False):
    """
    Ordem de execução:
        - agenda a próxima execução do experimento de acordo com ~exp(30)
        - realiza o teste ndt + traceroute para domínio ndt
        - navega todas as 20 páginas, uma de cada vez, via puppeteer
        - reproduz um dos 20 vídeos, via selenium
    """

    mac = QUEUE[4:]
    now = datetime.now()
    result = {
        'task': 'experimento_1',
        'started': now.timestamp(),
        'mac': mac,
    }

    # ndt
    result['ndt'] = ndt_experiment(IPV6)
    result['browser'] = {}
    result['browser']['navigation'] = {}
    num_pages = get_number_of_pages_from_file()
    for _ in range(num_pages):
        # setup
        url = get_url_for_experiment_type('navigation')
        unlock_chrome_profile()
        # navigation experiment
        result['browser']['navigation'][url] = {}
        result['browser']['navigation'][url]['started'] = now.timestamp()
        result['browser']['navigation'][url]['data'] = puppeteer_navigation(url)

    # reproduction experiment
    url = get_url_for_experiment_type('reproduction')
    result['browser']['reproduction'] = {}
    index = url.find('watch?v=')
    result['browser']['reproduction']['video_id'] = url[index+8:]
    result['browser']['reproduction']['started'] = now.timestamp()
    result['browser']['reproduction']['data'] = selenium_reproduction(url)

    result['ended'] = datetime.now().timestamp()
    
    # save and send
    save_and_send(result, app)

    # schedule APS
    if schedule_next:
        time_in_minutes = expon.rvs(scale=int(EXPONENTIAL_MEAN_EXPERIMENTO_1_INTERVAL), size=1)[0]
        next_run = now + timedelta(minutes=time_in_minutes)
        next_run_time = next_run.strftime("%H:%M")
        schedule.every().day.at(next_run_time).do(experimento_1, True)
        logger.info(f'Next execution: {next_run}')

    return result

if not scheduler.running:
    scheduler.start()
    experimento_1(True)

@app.task(name='data_gathering.send_tasks')
@app.task(name=f'{QUEUE}.data_gathering.send_tasks')
def send_tasks_to_server():
    send_results_and_delete(app, 'writers.save')

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
        'ndt7': 'data_gathering.data_gathering.tasks:ndt7',
        'experimento_1': 'data_gathering.data_gathering.tasks:experimento_1',
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
