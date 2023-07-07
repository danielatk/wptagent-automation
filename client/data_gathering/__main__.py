import argparse
from dotenv import load_dotenv

load_dotenv()
from data_gathering.celery import app

def main():
    parser = argparse.ArgumentParser(
        prog='data_gathering',
        description='Send tasks to devices',
    )
    parser.add_argument('task', help='Task route')
    parser.add_argument('args', nargs='*', default=[], help='Task arguments')
    parser.add_argument('--exchange', type=str, default='data_gathering')
    ns = parser.parse_args()
    task = app.send_task(ns.task, ns.args, routing_key=ns.task, exchange=ns.exchange)
    print(task.get())

if __name__ == '__main__':
    main()
