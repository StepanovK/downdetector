from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models import MonitoredApp


class App(Resource):
    @classmethod
    def get(cls, name):
        app = MonitoredApp.find_by_name(name)
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

        if MonitoredApp.get_by_name(args['name']):
            return {
                       'message': f'An app with name {args["name"]} already exists.'
                   }, 400

        app = MonitoredApp(name=args['name'])
        app.checking_is_active = args['checking_is_active']
        app.checking_interval = args['checking_interval']
        try:
            token = app.save(generate_token=True)
        except SQLAlchemyError:
            return {'message': 'An error occurred creating the store.'}, 500

        app_json = app.json()
        app_json['token'] = token

        return app_json, 201

    @classmethod
    def delete(cls, name):
        app = MonitoredApp.get_by_name(name)
        if app:
            app.delete()
            return {'message': 'App deleted'}, 200
        return {'message': 'App not found'}, 404


class AppList(Resource):
    @classmethod
    def get(cls):
        return {'apps': [app.json() for app in MonitoredApp.get_all()]}
