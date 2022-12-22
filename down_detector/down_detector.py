from flask import Flask
from flask_restful import Api
from .models import db
from .resources import App, AppList, Log, StatusCheck


def create_app(database_uri="sqlite:///down_detector.db"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()

    create_api(app)

    return app


def create_api(app):
    api = Api(app)
    add_resources(api)
    return api


def add_resources(api):
    api.add_resource(App, '/app')
    api.add_resource(AppList, '/app_list')
    api.add_resource(Log, '/log')
    api.add_resource(StatusCheck, '/status_check')


if __name__ == '__main__':
    app_ = create_app()
    app_.run(debug=True, port=3030)
