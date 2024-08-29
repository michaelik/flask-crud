from repositories.user_repository import UserRepository
from mappers.user_mapper import UserMapper
from errors.user_not_found import UserNotFoundException
from models.db import db


class UserService:
    def __init__(self):
        self.user_repository = UserRepository(db.session)

    def create_user(self, user_dto):
        user = UserMapper.to_entity(user_dto)
        self.user_repository.save(user)

    def get_all_users(self):
        users = self.user_repository.find_all()
        return [UserMapper.to_dto(user) for user in users]

    def get_user(self, id):
        user = self.user_repository.find_by_id(id)
        if not user:
            raise UserNotFoundException(f"User with id {id} not found")
        return UserMapper.to_dto(user)

    def update_user(self, id, user_dto):
        user = self.user_repository.find_by_id(id)
        if not user:
            raise UserNotFoundException(f"User with id {id} not found")
        user.username = user_dto['username']
        user.email = user_dto['email']
        updated_user = self.user_repository.save(user)
        return UserMapper.to_dto(updated_user)

    def delete_user(self, id):
        user = self.user_repository.find_by_id(id)
        if not user:
            raise UserNotFoundException(f"User with id {id} not found")
        self.user_repository.delete(user)
        return True
