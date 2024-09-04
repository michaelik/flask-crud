from config import LogConfig
from models.user import db, User

logger = LogConfig.configure_logging()


class TestUserController:

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
