from ..schemas import PointSchema


class Points:
    schema = PointSchema()

    def __init__(self, *, count, createdAt, token, username, **kwargs):
        if "id" in kwargs:
            self.id = kwargs["id"]
        self.username = username
        self.createdAt = createdAt
        self.token = token
        self.count = count