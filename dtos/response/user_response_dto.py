from marshmallow import Schema, fields


class UserResponseDTO(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
