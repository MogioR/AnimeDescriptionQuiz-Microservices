import os
import time

from .uuid_token import UUIDToken

EXPIRES_TIME = int(os.getenv("TOKEN_EXPIRES_TIME"))
TOTAL_EXPIRES_TIME = int(os.getenv("TOKEN_TOTAL_EXPIRES_TIME"))


class TokenService:
    def __init__(self):
        self.tokens = []

    def create_token(self, data):
        self.del_token(data)
        token = UUIDToken(data, EXPIRES_TIME)
        self.tokens.append(token)
        if len(self.tokens) > 100:
            self.update()
        return token

    def get_data(self, data):
        for token in self.tokens:
            if token.data == data:
                return data, token.has_expire()
        return None

    def refresh_token(self, refresh_token: str):
        for token in self.tokens:
            if token.refresh_token == refresh_token and time.time() - token.expires_time < TOTAL_EXPIRES_TIME:
                token = UUIDToken(token.data, EXPIRES_TIME)
                return token
        return None

    def check_token(self, access_token: str):
        for token in self.tokens:
            if token.access_token == access_token:
                return token.data, token.has_expire()
        return None, None

    def del_token(self, data):
        del_index = -1
        for index, token in enumerate(self.tokens):
            if token.data == data:
                del_index = index

        if del_index > -1:
            self.tokens.pop(del_index)

    def update(self):
        self.tokens = [token for token in self.tokens if time.time() - token.expires_time < TOTAL_EXPIRES_TIME]

