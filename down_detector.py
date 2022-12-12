from flask import Flask
from flask_restful import Api, Resource, reqparse
from db import db
from resources.monitored_app import App, AppList
from resources.app_log import Log


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)
api = Api(app)

with app.app_context():
    import models
    db.create_all()

api.add_resource(App, '/app')
api.add_resource(AppList, '/app_list')
api.add_resource(Log, '/log')

if __name__ == '__main__':
    app.run(debug=True, port=3030)
