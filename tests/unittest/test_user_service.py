import unittest
from unittest.mock import patch, MagicMock
from services.user_service import UserService
from errors.user_not_found import UserNotFoundException


class TestUserService(unittest.TestCase):

    def setUp(self):
        self.user_service = UserService()

    @patch('repositories.user_repository.UserRepository.save')
    @patch('mappers.user_mapper.UserMapper.to_entity')
    def test_create_user_successful(self, mock_to_entity, mock_save):
        # Given (Arrange)
        user_dto = {'username': 'johndoe', 'email': 'john@example.com'}
        user_entity = MagicMock()
        mock_to_entity.return_value = user_entity

        # When (Act)
        self.user_service.create_user(user_dto)

        # Then (Assert)
        mock_to_entity.assert_called_once_with(user_dto)
        mock_save.assert_called_once_with(user_entity)

    @patch('repositories.user_repository.UserRepository.find_all')
    @patch('mappers.user_mapper.UserMapper.to_dto')
    def test_get_all_users_successful(self, mock_to_dto, mock_find_all):
        # Given (Arrange)
        users = [MagicMock(), MagicMock()]
        user_dtos = [{'username': 'johndoe', 'email': 'john@example.com'},
                     {'username': 'joyboy', 'email': 'joy@example.com'}]
        mock_find_all.return_value = users
        mock_to_dto.side_effect = user_dtos

        # When (Act)
        result = self.user_service.get_all_users()

        # Then (Assert)
        self.assertEqual(result, user_dtos)
        mock_find_all.assert_called_once()
        self.assertEqual(mock_to_dto.call_count, len(users))

    @patch('repositories.user_repository.UserRepository.find_by_id')
    @patch('mappers.user_mapper.UserMapper.to_dto')
    def test_get_user_existing_user_successful(self, mock_to_dto, mock_find_by_id):
        # Given (Arrange)
        user_id = 1
        user = MagicMock()
        user_dto = {'username': 'johndoe', 'email': 'john@example.com'}
        mock_find_by_id.return_value = user
        mock_to_dto.return_value = user_dto

        # When (Act)
        result = self.user_service.get_user(user_id)

        # Then (Assert)
        self.assertEqual(result, user_dto)
        mock_find_by_id.assert_called_once_with(user_id)
        mock_to_dto.assert_called_once_with(user)

    @patch('repositories.user_repository.UserRepository.find_by_id')
    def test_get_user_non_existing_user_throws_user_not_found_exception(self, mock_find_by_id):
        # Given (Arrange)
        user_id = 1
        mock_find_by_id.return_value = None

        # When (Act)
        with self.assertRaises(UserNotFoundException) as context:
            self.user_service.get_user(user_id)

        # Then (Assert)
        self.assertEqual(str(context.exception), f"User with id {user_id} not found")
        mock_find_by_id.assert_called_once_with(user_id)

    @patch('repositories.user_repository.UserRepository.save')
    @patch('repositories.user_repository.UserRepository.find_by_id')
    @patch('mappers.user_mapper.UserMapper.to_dto')
    def test_update_user_existing_user_successful(self, mock_to_dto, mock_find_by_id, mock_save):
        # Given (Arrange)
        user_id = 1
        user_dto = {'username': 'johndoe', 'email': 'john@example.com'}
        user = MagicMock()
        updated_user = MagicMock()
        updated_user_dto = user_dto.copy()
        mock_find_by_id.return_value = user
        mock_save.return_value = updated_user
        mock_to_dto.return_value = updated_user_dto

        # When (Act)
        result = self.user_service.update_user(user_id, user_dto)

        # Then (Assert)
        self.assertEqual(result, updated_user_dto)
        mock_find_by_id.assert_called_once_with(user_id)
        mock_save.assert_called_once_with(user)
        mock_to_dto.assert_called_once_with(updated_user)

    @patch('repositories.user_repository.UserRepository.find_by_id')
    def test_update_user_non_existing_user_throws_user_not_found_exception(self, mock_find_by_id):
        # Given (Arrange)
        user_id = 1
        user_dto = {'username': 'johndoe', 'email': 'john@example.com'}
        mock_find_by_id.return_value = None

        # When (Act)
        with self.assertRaises(UserNotFoundException) as context:
            self.user_service.update_user(user_id, user_dto)

        # Then (Assert)
        self.assertEqual(str(context.exception), f"User with id {user_id} not found")
        mock_find_by_id.assert_called_once_with(user_id)

    @patch('repositories.user_repository.UserRepository.delete')
    @patch('repositories.user_repository.UserRepository.find_by_id')
    def test_delete_user_existing_user_successful(self, mock_find_by_id, mock_delete):
        # Given (Arrange)
        user_id = 1
        user = MagicMock()
        mock_find_by_id.return_value = user

        # When (Act)
        result = self.user_service.delete_user(user_id)

        # Then (Assert)
        self.assertTrue(result)
        mock_find_by_id.assert_called_once_with(user_id)
        mock_delete.assert_called_once_with(user)

    @patch('repositories.user_repository.UserRepository.find_by_id')
    def test_delete_user_non_existing_user_throws_user_not_found_exception(self, mock_find_by_id):
        # Given (Arrange)
        user_id = 1
        mock_find_by_id.return_value = None

        # When (Act)
        with self.assertRaises(UserNotFoundException) as context:
            self.user_service.delete_user(user_id)

        # Then (Assert)
        self.assertEqual(str(context.exception), f"User with id {user_id} not found")
        mock_find_by_id.assert_called_once_with(user_id)
