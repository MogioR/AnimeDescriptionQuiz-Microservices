import time


class Token:
    def __init__(self, data, expires_timer):
        self.data = data
        self.expires_time = time.time() + expires_timer

    def has_expire(self) -> bool:
        return time.time() >= self.expires_time

    def extension(self, expires_timer):
        self.expires_time = time.time() + expires_timer
