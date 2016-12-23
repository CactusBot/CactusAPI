from marshmallow import Schema, fields

from .helpers import ValidateToken


class UserSchema(Schema):
    id = fields.String()
    token = ValidateToken()
    userName = fields.String(required=True)
    userId = fields.Integer(required=True)
    service = fields.String(required=True, default="beam")
    password = fields.String(default=None)
