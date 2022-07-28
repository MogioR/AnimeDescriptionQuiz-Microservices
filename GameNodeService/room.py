from Package.package import Package
from user import User
from room_settings import RoomSettings
from default_quiz import DefaultQuiz


class Room:
    def __init__(self, room_settings: dict):
        self.host = None
        self.users = []
        self.options = []
        self.status = "created"
        self.settings = RoomSettings(room_settings)

        self.quiz = DefaultQuiz()

    def connect(self, user: User) -> list:
        if self.host is None:
            self.host = user
            self.status = "in_lobby"

        if len(self.users) < self.settings.room_size:
            self.users.append(user)

            message_to_connected = Package(user.socket, {'action': 'room', 'type': 'enter_to_room',
                                                         'room_settings': self.settings, 'host': self.host})
            messages_to_users = [message_to_connected]
            message_to_users = {'action': 'room', 'type': 'user_connect', 'user': user, 'new_user_list': self.users}

            for user in self.users:
                messages_to_users.append(Package(user.socket, message_to_users))
            return messages_to_users
        else:
            return [Package(user.socket, {'action': 'system', 'type': 'error', 'text': 'Room is full.'})]

    def disconnect(self, user: User) -> list:
        messages_to_users = []

        self.users.remove(user)
        new_host = False
        if user is self.host:
            new_host = True
            if len(self.users) > 0:
                self.host = self.users[0]
            else:
                self.host = None

        message_to_users = {'action': 'room', 'type': 'user_disconnect', 'user': user, 'new_user_list': self.users}
        if new_host:
            message_to_users.update({'new_host': self.host})

        for user in self.users:
            messages_to_users.append(Package(user.socket, message_to_users))

        return messages_to_users

    def update(self):
        self.quiz.update()

    def start_quiz(self):
        self.quiz.start_quiz()

    def stop_quiz(self):
        self.stop_quiz()

    def resume_quiz(self):
        self.quiz.resume_quiz()
