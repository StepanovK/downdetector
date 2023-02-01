from config import logger
from down_detector.models import MonitoredApp, User
from down_detector import create_app, db
from sqlalchemy.exc import SQLAlchemyError

from typing import Union, Optional


def app():
    _app = create_app()

    with _app.app_context():
        db.create_all()

    return _app


def register_user(login: str = '',
                  first_name: str = '',
                  last_name: str = '',
                  telegram_id: Optional[int] = None,
                  ) -> Union[dict, str]:
    _app = app()
    with _app.app_context():
        user = User(login=login)
        user.first_name = first_name
        user.last_name = last_name
        user.telegram_id = telegram_id
        try:
            user.save()
            return user.json()
        except SQLAlchemyError as er:
            err_text = f'An error occurred creating the user:\n{er}'
            logger.error(err_text)
            return err_text


def register_monitored_app(app_name: str,
                           checking_is_active: bool = False,
                           checking_interval: bool = 60,
                           ) -> Union[dict, str]:
    _app = app()
    with _app.app_context():
        monitored_app = MonitoredApp(name=app_name)
        monitored_app.checking_is_active = checking_is_active
        monitored_app.checking_interval = checking_interval
        try:
            token = monitored_app.save(generate_token=True)
        except SQLAlchemyError as er:
            err_text = f'An error occurred creating the app:\n{er}'
            logger.error(err_text)
            return err_text

    app_json = monitored_app.json()
    app_json['token'] = token

    return app_json
