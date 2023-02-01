import sys
import os

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)

from flask import Flask
from flask_restful import Api
from models import db
from resources import App, AppList, Log, StatusCheck
import os


def create_app(database_uri=None):
    if database_uri is None:
        database_path = os.path.split(basedir)[0]
        database_path = os.path.join(database_path, 'down_detector.db')
        database_uri = f"sqlite:///{database_path}"
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
