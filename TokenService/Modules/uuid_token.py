import uuid
from .token import Token


class UUIDToken(Token):
    def __init__(self, data, expires_timer):
        super().__init__(data, expires_timer)
        self.access_token = str(uuid.uuid4())
        self.refresh_token = str(uuid.uuid4())