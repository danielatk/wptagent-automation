from urllib.parse import urlparse
from scipy.stats import expon
from data_gathering.celery import app, logger, QUEUE
from .utils import *

EXPONENTIAL_MEAN_EXPERIMENTO_1_INTERVAL = 30


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

@app.task(name='experimento_1.ndt7')
@app.task(name=f'{QUEUE}.experimento_1.ndt7')
def experimento_1():
    """
    Ordem de execução:
        - agenda a próxima execução do experimento de acordo com ~exp(30)
        - traceroute
        - tira na moeda entre setupNavigationFilePath e setupReproductionFilePath -> X
        - realiza o setup do teste X (obtém url)
        - realiza o teste X no puppeteer
        - realiza o teste X no selenium
        - realiza o teste ndt
    """
    time_in_minutes = expon.rvs(scale=int(EXPONENTIAL_MEAN_EXPERIMENTO_1_INTERVAL), size=1)[0]
    # agenda APS
    # navigation or reproduction?
    experiment = get_experiment_type_at_random()
    # setup
    url = get_url_for_experiment_type(experiment)
    domain = urlparse(url).netloc
    # traceroute
    traceroute_result = call_traceroute(domain)
    browser_result = run_browser_experiment(experiment)
    call_ndt7()
