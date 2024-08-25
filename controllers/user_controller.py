from flask_restful import Resource
from flask import request
from dtos.request.user_request_dto import UserRequestDTO
from services.user_service import UserService
from dtos.response_helper import ResponseHelper


class UserController(Resource):
    def __init__(self):
        self.user_service = UserService()
        self.user_request_dto = UserRequestDTO()

    def post(self):
        user_dto = self.user_request_dto.load(request.get_json())
        self.user_service.create_user(user_dto)
        return ResponseHelper.base_response(
            True,
            201,
            'User created successfully'
        )

    def get(self, id=None):
        if id:
            user = self.user_service.get_user(id)
            return ResponseHelper.base_response(
                True,
                200,
                'User retrieved successfully',
                user
            )
        else:
            users = self.user_service.get_all_users()
            return ResponseHelper.base_response(
                True,
                200,
                'Users retrieved successfully',
                users
            )

    def put(self, id):
        user_dto = self.user_request_dto.load(request.get_json())
        updated_user = self.user_service.update_user(id, user_dto)
        return ResponseHelper.base_response(
            True,
            200,
            'User updated successfully',
            updated_user
        )

    def delete(self, id):
        self.user_service.delete_user(id)
        return ResponseHelper.base_response(
            True,
            200,
            'User deleted successfully'
        )
