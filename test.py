import datetime

import requests
import json
import random
import secrets

from db import db
from models import ApplicationLog


def add_app():
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'name': 'test4',
        'checking_is_active': 1,
        'checking_interval': 30,
    }

    res = requests.post('http://127.0.0.1:3030/app',
                        json=data,
                        headers=headers)
    print(res)
    print(res.text)
    app_info = json.loads(res.text)

    return app_info


def add_logs(app_info, count):
    td = datetime.timedelta(days=120)
    now = datetime.datetime.now()
    start_date = now - td
    now_ts = now.timestamp()
    start_date_ts = start_date.timestamp()

    dates = []
    for i in range(count):
        dates.append(random.randint(int(start_date_ts), int(now_ts)))

    dates.sort()

    session = requests.session()
    session.headers = {
        'Content-Type': 'application/json',
    }

    for date in dates:
        message = f'Это тестовое сообщение от {datetime.datetime.fromtimestamp(date)}'

        data = {
            'app_name': app_info['name'],
            'token': app_info['token'],
            'date': date,
            'level': random.randint(0, 2),
            'short_message': message,
            'message': message,
        }

        res = session.post('http://127.0.0.1:3030/log', json=data)
        # print(res)
        # print(res.text)


def get_app(app_info):
    headers = {
        'Content-Type': 'application/json',
    }

    # now = datetime.datetime.now()

    data = {
        'app_name': app_info['name'],
        'token': app_info['token'],
        # 'date_from': now + ,
    }

    res = requests.get('http://127.0.0.1:3030/app',
                       json=data,
                       headers=headers)
    print(res)
    # print(res.text)
    app_info = json.loads(res.text)

    return app_info


def get_logs(app_info, date_from=None, date_to=None):
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'app_name': app_info['name'],
        'token': app_info['token'],
    }

    if date_from:
        data['date_from'] = date_from.timestamp()

    if date_to:
        data['date_to'] = date_to.timestamp()

    res = requests.get('http://127.0.0.1:3030/log',
                       json=data,
                       headers=headers)
    print('logs: ' + str(res))
    # print(res.text)
    logs = json.loads(res.text)

    return logs


if __name__ == '__main__':
    app_info_ = add_app()
    add_logs(app_info_, 1000)
    test_app_info = get_app(app_info_)

    now = datetime.datetime.now()
    logs1 = get_logs(app_info_,
                     date_from=(now + datetime.timedelta(days=-30)),
                     date_to=(now + datetime.timedelta(days=-5)))
    logs2 = get_logs(app_info_,
                     date_from=(now + datetime.timedelta(days=-30)))
    logs3 = get_logs(app_info_,
                     date_to=(now + datetime.timedelta(days=-5)))
