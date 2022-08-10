import json
from smart_socket import SmartSocket


class User:
    def __init__(self, socket: SmartSocket, account_data: dict):
        self.socket: SmartSocket = socket
        self.user_id = socket.user_id
        self.username = account_data['username']
        self.experience = account_data['experience']
        self.room = -1

    def __str__(self):
        return str({'user_id': self.user_id, 'username': self.username, 'experience': self.experience})

    def __repr__(self):
        return str(self)


class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {'user_id': obj.user_id, 'username': obj.username, 'experience': obj.experience}
        return json.JSONEncoder.default(self, obj)
