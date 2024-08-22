from marshmallow import Schema, fields


class UserRequestDTO(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
