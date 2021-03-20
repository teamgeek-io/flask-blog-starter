import pytest

from flask_blog import create_app
from flask_blog.database import db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    db.create_all(app=app)
    yield app
    db.drop_all(app=app)


@pytest.fixture
def app_context(app):
    with app.app_context() as app_context:
        yield app_context


@pytest.fixture
def request_context(app):
    with app.test_request_context() as request_context:
        yield request_context


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
