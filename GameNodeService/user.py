class User:
    def __init__(self, socket, user_id: int, account_data: dir):
        self.socket = socket
        self.user_id = user_id
        self.username = account_data['username']
        self.experience = account_data['experience']

    def __str__(self):
        return str({'user_id': self.user_id, 'username': self.username, 'experience': self.experience})

    def __repr__(self):
        return str(self)
