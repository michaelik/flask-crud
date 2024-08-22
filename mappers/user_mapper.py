from dtos.response.user_response_dto import UserResponseDTO
from dtos.request.user_request_dto import UserRequestDTO
from models.user import User


class UserMapper:
    """
    Marshmallow schemas typically work with dictionaries.
    Marshmallow Schema: Use the load method for deserialization if needed.
    """
    @staticmethod
    def to_entity(user_dto: dict) -> User:
        return User(username=user_dto['username'], email=user_dto['email'])

    @staticmethod
    def to_dto(user: User) -> dict:
        return UserResponseDTO().dump(user)
