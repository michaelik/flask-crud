import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from app import create_app
from models.user import db


@pytest.fixture(scope='module')
def test_app():
    """Fixture to create a new app instance for testing."""
    app = create_app(environment='testing')
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture(autouse=True)
def session_setup(test_app):
    """Automatically wraps each test in a database transaction, which is rolled back after the test."""
    with test_app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        session_factory = sessionmaker(bind=connection)
        session = scoped_session(session_factory)

        db.session = session

        yield session

        session.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(test_app):
    """Fixture to provide a test client."""
    return test_app.test_client()