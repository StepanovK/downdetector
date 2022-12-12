from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models import MonitoredApp
from typing import Optional, Union


class App(Resource):
    @classmethod
    def get(cls):
        app = cls.get_app_by_args()
        if isinstance(app, tuple):
            return app

        if app is None:
            return {'message': 'Some problem with getting app!'}, 400
        if app:
            return app.json()
        return {'message': 'App not found'}, 404

    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('checking_is_active', type=bool)
        parser.add_argument('checking_interval', type=int)
        args = parser.parse_args()

        app_name = args["name"]
        if not app_name:
            return {'message': f'"name" is empty'}, 400

        if MonitoredApp.get_by_name(app_name):
            return {
                       'message': f'An app with name {app_name} already exists.'
                   }, 400

        app = MonitoredApp(name=app_name)
        if args['checking_is_active']:
            app.checking_is_active = args['checking_is_active']
        if args['checking_interval']:
            app.checking_interval = args['checking_interval']
        else:
            app.checking_interval = 0

        try:
            token = app.save(generate_token=True)
        except SQLAlchemyError:
            return {'message': 'An error occurred creating the store.'}, 500

        app_json = app.json()
        app_json['token'] = token

        return app_json, 201

    @classmethod
    def delete(cls):
        app = cls.get_app_by_args()
        if isinstance(app, tuple):
            return app
        if app:
            app.delete()
            return {'message': 'App deleted'}, 200
        return {'message': 'App not found'}, 404

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


class AppList(Resource):
    @classmethod
    def get(cls):
        return {'apps': [app.json() for app in MonitoredApp.get_all()]}
