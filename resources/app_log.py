import datetime

from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models import MonitoredApp, ApplicationLog
from typing import Optional, Union
from db import db


class Log(Resource):
    @classmethod
    def get(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('app_name', type=str)
        parser.add_argument('token', type=str)
        parser.add_argument('date_from', type=float)
        parser.add_argument('date_to', type=float)
        args = parser.parse_args()

        app = cls.get_app_by_args(args)
        if isinstance(app, tuple):
            return app

        query = db.session.query(ApplicationLog).filter(ApplicationLog.app_id == app.id)
        date_from = args.get('date_from', 0)
        if date_from and date_from >= 0:
            query = query.filter(ApplicationLog.date >= datetime.datetime.fromtimestamp(date_from))
        date_to = args.get('date_to', 0)
        if date_to and date_to >= 0:
            query = query.filter(ApplicationLog.date <= datetime.datetime.fromtimestamp(date_to))

        result = query.order_by(ApplicationLog.date).all()

        return [rec.json() for rec in result]

    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('app_name', type=str)
        parser.add_argument('token', type=str)
        parser.add_argument('date', type=float)
        parser.add_argument('level', type=int)
        parser.add_argument('short_message', type=str)
        parser.add_argument('message', type=str)
        args = parser.parse_args()

        app = cls.get_app_by_args(args)
        if isinstance(app, tuple):
            return app

        if app is None:
            return {'message': 'Some problem with getting app!'}, 400

        date_ts = args.get('date', 0)
        if (isinstance(date_ts, float) or isinstance(date_ts, int)) and date_ts != 0:
            date = datetime.datetime.fromtimestamp(date_ts)
        else:
            return {'message': '"date" is empty!'}, 400

        level = args.get('level', 0)
        if level is None:
            level = 0

        log_record = ApplicationLog(app_id=app.id,
                                    date=date,
                                    level=level)
        if args.get('short_message', '') is None:
            log_record.short_message = ''
        else:
            log_record.short_message = args.get('short_message', '')[:255]

        if args.get('message', '') is None:
            log_record.message = ''
        else:
            log_record.message = args.get('message', '')[:255]
        log_record.save()

        return log_record.json(), 201

    @classmethod
    def get_app_by_args(cls, args: Optional[dict] = None) -> Union[MonitoredApp, tuple]:
        if args is None:
            parser = reqparse.RequestParser()
            parser.add_argument('app_name', type=str)
            parser.add_argument('token', type=str)
            args = parser.parse_args()

        app_name = args.get('app_name', '')
        if not app_name:
            return {'message': f'"app_name" is empty'}, 400

        app = MonitoredApp.get_by_name(app_name)
        if not app:
            return {'message': f'App {app_name} not found'}, 404

        token = args.get('token', '')

        if not token:
            return {'message': f'"token" is empty'}, 400

        if not app.check_token(token):
            return {'message': f'Invalid token'}, 401

        return app
