import pytest

from down_detector import create_app, db


@pytest.fixture()
def app():
    app = create_app("sqlite://")
    app.testing = True
    db.init_app(app)
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
