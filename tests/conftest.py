import pytest

from down_detector import create_app, db


@pytest.fixture()
def app():
    app = create_app("sqlite://")

    with app.app_context():
        db.create_all()
    app.testing = True

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
