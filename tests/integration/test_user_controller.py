import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from app import create_app
from config import config, LogConfig
from models.user import db, User

logger = LogConfig.configure_logging()


class TestUserController:

    @pytest.fixture(scope='module')
    def test_app(self):
        """Fixture to create a new app instance for testing."""
        app = create_app()
        if not app.config.from_object(config['development']):
            logger.info("Using configuration: %s", config['testing'].__dict__)
            with app.app_context():
                db.create_all()
                yield app

    @pytest.fixture(autouse=True)
    def session_setup(self, test_app):
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
    def client(self, test_app):
        """Fixture to provide a test client."""
        return test_app.test_client()

    def test_create_user(self, client):
        # Given
        user_data = {
            'username': 'test_user',
            'email': 'testuser@example.com'
        }

        # When
        response = client.post('/users', json=user_data)

        # Then
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['success'] is True
        assert json_data['message'] == 'User created successfully'

    def test_get_all_users(self, client):
        # Given
        user1 = User(username='user1', email='user1@example.com')
        user2 = User(username='user2', email='user2@example.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # When
        response = client.get('/users')

        # Then
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert len(json_data['data']) == 2

    def test_get_user_by_id(self, client):
        # Given
        user = User(username='test_user', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        # When
        response = client.get(f'/users/{user.id}')

        # Then
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert json_data['data']['username'] == 'test_user'

    def test_update_user(self, client):
        # Given
        user = User(username='test_user', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        updated_data = {
            'username': 'updated_user',
            'email': 'updateduser@example.com'
        }

        # When
        response = client.put(f'/users/{user.id}', json=updated_data)

        # Then
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert json_data['data']['username'] == 'updated_user'

    def test_delete_user(self, client):
        # Given
        user = User(username='test_user', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        # When
        response = client.delete(f'/users/{user.id}')

        # Then
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
