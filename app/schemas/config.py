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


class SpamSchema(Schema):
    maxEmoji = fields.Integer(default=6)
    maxCapsScore = fields.Integer(default=16)
    allowUrls = fields.Boolean(default=False)


class WhitelistSchema(Schema):
    whitelisted_urls = fields.List(fields.String(), default=[])
    whitelisted_words = fields.List(fields.String(), default=[])


class BlacklistSchema(Schema):
    blacklisted_urls = fields.List(fields.String(), default=[])
    blacklisted_words = fields.List(fields.String(), default=[])


class ConfigSchema(Schema):
    id = fields.String()
    token = fields.String(required=True)
    services = fields.Nested(ServiceSchema, many=True)
    announce = fields.Nested(AnnouncementsSchema)
    spam = fields.Nested(SpamSchema)
    whitelist = fields.Nested(WhitelistSchema)
    blacklist = fields.Nested(BlacklistSchema)
