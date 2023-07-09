import random
import subprocess
import json
from typing import Tuple

from celery.result import allow_join_result
from data_gathering.celery import logger
from .navigation import selenium_reproduction
from ..model import get_random_video, get_random_page, get_random_uf, save_result, remove_saved_results, get_all_saved_results

VERSION_FILE = '/app/version'
VERSION = None
EXPERIMENT_TYPES = ['navigation', 'reproduction']

EXTENSION_DB = '/data/chrome/data_gathering_agent/Sync Extension Settings/ojaljkmpomphjjkkgkdhenlhogcajbmf'

def call_program(program) -> Tuple[bytes, bytes]:
    result = subprocess.run(program, capture_output=True)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')

def call_ndt7(server = None) -> bytes:
    command = ['ndt7-client', '-no-verify', '-scheme', 'wss', '-format', 'json']
    if server:
        command += ['-server', server]
    result, _ = call_program(command)
    return result

def parser_ndt_output(output):
    return [json.loads(x) for x in output.split()]

def ndt_experiment(has_ipv6: bool):
    uf = get_random_uf()
    result = {
        'uf': uf,
    }
    if uf == 'mlab':
        ndt = call_ndt7()
        result['ndt'] = parser_ndt_output(ndt)
        # get server fqdn
        server = get_server_fqdn_from_ndt(result['ndt'])
        result['traceroute-4'] = call_traceroute(server)
        if has_ipv6:
            result['traceroute-6'] = call_traceroute(server, True)
    else:
        server = f'{uf}.medidor.rnp.br'
        ndt = call_ndt7(f'{server}:4443')
        result['ndt'] = parser_ndt_output(ndt)
        result['traceroute-4'] = call_traceroute(server)
    return result

def get_server_fqdn_from_ndt(ndt):
    for line in ndt:
        if 'Key' not in line:
            continue
        if line['Key'] == 'connected' and line['Value']['Test'] == 'download':
            return line['Value']['Server']
    return None

def call_traceroute(server, ip_v6 = False):
    command = ['traceroute', '-6' if ip_v6 else '-4', server]
    result, _ = call_program(command)
    return result

def unlock_chrome_profile():
    result, _ = call_program(['rm', '/data/chrome/SingletonLock'])
    return result

def get_runtime_version():
    global VERSION
    if VERSION:
        return VERSION
    with open(VERSION_FILE, 'r', encoding='utf-8') as f:
        VERSION = f.read()
    return VERSION

def get_url_for_experiment_type(experiment_type):
    return dict(zip(EXPERIMENT_TYPES, [
        get_random_page,
        get_random_video,
    ]))[experiment_type]()

def call_puppeteer(url):
    command = ['node', '/app/resources/puppeteer/index.js', url]
    result, _ = call_program(command)
    return result

def puppeteer_navigation(url):
    return call_puppeteer(url)

def send_results_and_delete(app, task):
    saved_results = get_all_saved_results()
    for r in saved_results:
        try:
                # with allow_join_result():
                # t = app.send_task(task, [json.loads(r.payload)], routing_key=task, exchange='writers')
                # t.get()
                app.send_task(task, [json.loads(r.payload)], routing_key=task, exchange='data_gathering')
                remove_saved_results([r])
        except Exception as err:
            logger.info('Error when sending task to server: %s', err, exc_info=1)

def save_and_send(result: dict, app):
    save_result(result)
    send_results_and_delete(app, 'writers.save')