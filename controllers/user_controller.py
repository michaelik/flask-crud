from flask_restful import Resource
from flask import request
from dtos.request.user_request_dto import UserRequestDTO
from services.user_service import UserService
from errors.user_not_found import UserNotFoundException
from marshmallow import ValidationError


class UserController(Resource):
    def __init__(self):
        self.user_service = UserService()
        self.user_request_dto = UserRequestDTO()

    def post(self):
        try:
            user_dto = self.user_request_dto.load(request.get_json())
            self.user_service.create_user(user_dto)
            return {'message': 'user created'}, 201
        except ValidationError as e:
            raise e  # Let error handler process this
        except Exception as e:
            return {'message': 'An error occurred', 'details': str(e)}, 500

    def get(self, id=None):
        try:
            if id:
                user = self.user_service.get_user(id)
                return {'user': user}, 200
            else:
                users = self.user_service.get_all_users()
                return users, 200
        except UserNotFoundException as e:
            return {'message': str(e)}, 404
        except Exception as e:
            return {'message': 'An error occurred', 'details': str(e)}, 500

    def put(self, id):
        try:
            user_dto = request.get_json()
            self.user_service.update_user(id, user_dto)
            return {'message': 'user updated'}, 200
        except UserNotFoundException as e:
            return {'message': str(e)}, 404
        except Exception as e:
            return {'message': 'An error occurred', 'details': str(e)}, 500

    def delete(self, id):
        try:
            self.user_service.delete_user(id)
            return {'message': 'user deleted'}, 200
        except UserNotFoundException as e:
            return {'message': str(e)}, 404
        except Exception as e:
            return {'message': 'An error occurred', 'details': str(e)}, 500
