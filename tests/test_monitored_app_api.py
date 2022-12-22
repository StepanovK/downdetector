import datetime

from down_detector.models import MonitoredApp, ApplicationLog, ApplicationStatusCheck
import json
from faker import Faker
from time import sleep


def test_create_app(client, app):
    res = _add_app(client)
    assert res.status_code == 201
    assert res.data is not None
    app_info = json.loads(res.text)
    assert 'token' in app_info
    assert 'name' in app_info
    with app.app_context():
        assert MonitoredApp.query.count() == 1
        assert MonitoredApp.query.first().check_token(app_info['token'])


def test_add_logs(client, app):
    count_log_records = 100
    res = _add_app(client)
    app_info = json.loads(res.text)
    test_logs = _get_test_logs(app_info, count=count_log_records)
    for test_log in test_logs:
        res = client.post('http://127.0.0.1:3030/log', json=test_log)
        assert res.status_code == 201
        log_record = json.loads(res.text)
        assert 'app_name' in log_record
        assert log_record['app_name'] == app_info['name']
    with app.app_context():
        assert ApplicationLog.query.count() == count_log_records


def test_add_logs_errors(client, app):
    res = _add_app(client)
    app_info = json.loads(res.text)

    fake = Faker('ru_RU')
    log = {
        'app_name': app_info['name'],
        'token': app_info['token'],
        'date': datetime.datetime.now().timestamp(),
        'level': fake.random.randint(0, 2),
        'short_message': fake.text(200),
        'message': fake.text(500),
    }

    wrong_log = log.copy()
    wrong_log['app_name'] = fake.name()
    res = client.post('http://127.0.0.1:3030/log', json=wrong_log)
    assert res.status_code == 404

    wrong_log = log.copy()
    wrong_log.pop('app_name')
    res = client.post('http://127.0.0.1:3030/log', json=wrong_log)
    assert res.status_code == 400

    wrong_log = log.copy()
    wrong_log.pop('token')
    res = client.post('http://127.0.0.1:3030/log', json=wrong_log)
    assert res.status_code == 400

    wrong_log = log.copy()
    wrong_log['level'] = 9
    res = client.post('http://127.0.0.1:3030/log', json=wrong_log)
    assert res.status_code == 400

    wrong_log = log.copy()
    wrong_log['date'] = 0
    res = client.post('http://127.0.0.1:3030/log', json=wrong_log)
    assert res.status_code == 400


def test_get_logs(client, app):
    count_log_records = 10
    res = _add_app(client)
    app_info = json.loads(res.text)
    test_logs = _get_test_logs(app_info, count=count_log_records)
    for test_log in test_logs:
        client.post('http://127.0.0.1:3030/log', json=test_log)

    logs_params = {
        'app_name': app_info['name'],
        'token': app_info['token'],
    }

    fake = Faker('ru_RU')

    fake_logs_params = logs_params.copy()
    fake_logs_params['token'] = fake.name()
    res = client.get('http://127.0.0.1:3030/log', json=fake_logs_params)
    assert res.status_code == 401

    fake_logs_params = logs_params.copy()
    fake_logs_params['app_name'] = fake.name()
    res = client.get('http://127.0.0.1:3030/log', json=fake_logs_params)
    assert res.status_code == 404

    res = client.get('http://127.0.0.1:3030/log', json=logs_params)
    assert res.status_code == 200
    logs_res = json.loads(res.text)
    assert 'count' in logs_res
    assert logs_res['count'] == count_log_records
    assert 'items' in logs_res
    assert len(logs_res['items']) == count_log_records

    with app.app_context():
        assert ApplicationLog.query.count() == count_log_records


def test_post_status_check(client, app):
    now = datetime.datetime.now()
    res = _add_app(client)
    app_info = json.loads(res.text)
    status_check = {
        'app_name': app_info['name'],
        'token': app_info['token'],
    }
    res = client.post('http://127.0.0.1:3030/status_check', json=status_check)
    assert res.status_code == 201
    log_json = json.loads(res.text)
    assert 'app_name' in log_json
    assert log_json['app_name'] == app_info['name']
    assert 'date' in log_json
    assert log_json['date'] >= now.timestamp()
    with app.app_context():
        assert ApplicationStatusCheck.query.count() == 1

    count_checks = 10
    for i in range(count_checks):
        sleep(0.1)
        client.post('http://127.0.0.1:3030/status_check', json=status_check)
    with app.app_context():
        assert ApplicationStatusCheck.query.count() == (count_checks + 1)


def _add_app(client):
    fake = Faker('ru_RU')
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'name': fake.name(),
        'checking_is_active': 1,
        'checking_interval': 30,
    }

    return client.post('http://127.0.0.1:3030/app',
                       json=data,
                       headers=headers)


def _get_test_logs(app_info, count, days=120):
    fake = Faker('ru_RU')
    td = datetime.timedelta(days=days)
    now = datetime.datetime.now()
    start_date = now - td
    now_ts = now.timestamp()
    start_date_ts = start_date.timestamp()

    dates = []
    for i in range(count):
        dates.append(fake.random.randint(int(start_date_ts), int(now_ts)))

    dates.sort()

    logs = []

    for date in dates:
        message = f'Это тестовое сообщение от {datetime.datetime.fromtimestamp(date)}'

        data = {
            'app_name': app_info['name'],
            'token': app_info['token'],
            'date': date,
            'level': fake.random.randint(0, 2),
            'short_message': message,
            'message': fake.text(300),
        }

        logs.append(data)

    return logs
