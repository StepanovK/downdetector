import datetime

from down_detector.models import MonitoredApp, ApplicationLog
import json
from faker import Faker


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
    #     log_record = json.loads(res.text)
    #     assert 'app_name' in log_record
    #     assert log_record['app_name'] == app_info['name']
    # with app.app_context():
    #     assert ApplicationLog.query.count() == count_log_records


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


def _get_test_logs(app_info, count):
    fake = Faker('ru_RU')
    td = datetime.timedelta(days=120)
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

# def test_registration(client, app):
#     response = client.post("/register", data={"email": "test@test.com", "password": "testpassword"})
#
#     with app.app_context():
#         assert User.query.count() == 1
#         assert User.query.first().email == "test@test.com"
#

# @responses.activate
# def test_age(client):
#     responses.add(
#         responses.GET,
#         "https://api.agify.io",
#         json={"age": 33, "count": 1049384, "name": "Anthony"},
#         status=200
#     )
#     client.post("/register", data={"email": "test@test.com", "password": "testpassword"})
#     client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
#
#     response = client.post("/age", data={"name": "Anthony"})
#
#     assert b"You are 33 years old" in response.data
#
#
# def test_invalid_login(client):
#     client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
#
#     response = client.get("/city")
#
#     assert response.status_code == 401
