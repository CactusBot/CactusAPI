from .. import app
from ..schemas import ConfigSchema


class Config:
    schema = ConfigSchema()

    ignore = ("password", )

    def __init__(self, token=None, services=None, announce=None, spam=None,
                 whitelisted_urls=[], whitelisted_words=[],
                 blacklisted_urls=[], blacklisted_words=[], **kwargs):
        # TODO: Don't add if None
        self.token = token
        self.services = services
        self.announce = announce
        self.spam = spam
        self.whitelisted_urls = whitelisted_urls
        self.whitelisted_words = whitelisted_words
        self.blacklisted_urls = blacklisted_urls
        self.blacklisted_words = blacklisted_words

    @staticmethod
    def default_data(token=None):
        return {
            "token": token.lower(),
            "services": [Service().__dict__],
            "announce": Announcements().__dict__,
            "spam": Spam().__dict__,
            "whitelist": Whitelist().__dict__,
            "blacklist": Blacklist().__dict__
        }


class Service:
    """
    Dummy class to keep track of sub-configs. Perhaps will implement proper
    loading later
    """

    def __init__(self,
                 name="beam",
                 isOAuth=False,
                 username=app.config.get("CB_USERNAME", "CactusBotDev"),
                 password=app.config.get("CB_PASSWORD", None),
                 permissions=["chat:connect", "chat:chat"]):
        self.name = name
        self.isOAuth = isOAuth
        self.username = username
        self.password = password
        self.permissions = permissions


class Announcements:
    """
    Dummy class to keep track of sub-configs. Perhaps will implement proper
    loading later
    """
    def default(announcement):
        return {
            "announce": False,
            "message": "Thanks for the {}, %USER%!".format(announcement)
        }

    def __init__(self,
                 follow=default("follow"),
                 join=default("join"),
                 leave=default("leave"),
                 sub=default("subscription"),
                 host=default("host")):
        self.follow = follow
        self.join = join
        self.leave = leave
        self.sub = sub
        self.host = host


class Spam:
    """
    Dummy class to keep track of sub-configs. Perhaps will implement proper
    loading later
    """

    def __init__(self,
                 maxEmoji=6,
                 allowUrls=False,
                 maxCapsScore=16):
        self.maxEmoji = maxEmoji
        self.allowUrls = allowUrls
        self.maxCapsScore = maxCapsScore


class Whitelist:
    """
    Dummy class to keep track of sub-configs. Perhaps will implement proper
    loading later
    """

    def __init__(self, whitelisted_urls=[], whitelisted_words=[]):
        self.whitelisted_urls = whitelisted_urls
        self.whitelisted_words = whitelisted_words


class Blacklist:
    """
    Dummy class to keep track of sub-configs. Perhaps will implement proper
    loading later
    """

    def __init__(self, blacklisted_urls=[], blacklisted_words=[]):
        self.blacklisted_urls = blacklisted_urls
        self.blacklisted_words = blacklisted_words
