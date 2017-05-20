from dateutil import parser
from marshmallow import Schema, fields

from ..util import helpers


class ServiceSchema(Schema):
    name = fields.String(required=True)
    isOAuth = fields.Boolean(default=False, required=True)
    username = fields.String()
    password = fields.String()
    permissions = fields.List(fields.String())


class Announcement(Schema):
    announce = fields.Boolean(default=False)
    message = fields.String()


class AnnouncementsSchema(Schema):
    join = fields.Nested(Announcement)
    follow = fields.Nested(Announcement)
    leave = fields.Nested(Announcement)
    sub = fields.Nested(Announcement)
    host = fields.Nested(Announcement)


class SpamMaxEmoji(Schema):
    value = fields.Integer(default=6)
    action = fields.String(default="purge")
    warnings = fields.Integer(default=3)


class SpamMaxCaps(Schema):
    value = fields.Integer(default=16)
    action = fields.String(default="purge")
    warnings = fields.Integer(default=3)


class SpamAllowURLs(Schema):
    value = fields.Boolean(default=False)
    action = fields.String(default="purge")
    warnings = fields.Integer(default=3)


class SpamBlacklist(Schema):
    value = fields.List(fields.String, default=[])
    action = fields.String(default="purge")
    warnings = fields.Integer(default=3)


class SpamSchema(Schema):
    maxEmoji = fields.Nested(SpamMaxEmoji)
    maxCapsScore = fields.Nested(SpamMaxCaps)
    allowUrls = fields.Nested(SpamAllowURLs)
    blacklist = fields.Nested(SpamBlacklist)


class ConfigSchema(Schema):
    id = fields.String()
    token = fields.String(required=True)
    services = fields.Nested(ServiceSchema, many=True)
    announce = fields.Nested(AnnouncementsSchema)
    spam = fields.Nested(SpamSchema)
    whitelistedUrls = fields.List(fields.String)
