from package import Package
from user import User
from room_settings import RoomSettings
from default_quiz import DefaultQuiz


class Room:
    def __init__(self, settings: dict):
        self.host = None
        self.users = []
        # self.options = []
        self.status = "created"
        self.room_settings = RoomSettings(settings['room_settings'])
        self.quiz = DefaultQuiz(settings['quiz_settings'], settings['question_settings'], self.users)

    def connect(self, connected_user: User):
        if self.host is None:
            self.host = connected_user
            self.status = "in_lobby"

        if len(self.users) < self.room_settings.room_size:
            self.users.append(connected_user)

            connected_user.socket.send({'action': 'room', 'type': 'enter_to_room',
                                        'settings': {
                                            'room': self.room_settings,
                                            'quiz': self.quiz.quiz_settings,
                                            'question': self.quiz.question_generator.question_settings
                                        },
                                        'host': self.host})

            message_to_users = {'action': 'room', 'type': 'user_connect', 'user': connected_user,
                                'new_user_list': self.users}

            for user in self.users:
                user.socket.send(message_to_users)

        else:
            connected_user.socket.send({'action': 'system', 'type': 'error', 'text': 'Room is full.'})

    def disconnect(self, disconnected_user: User):
        self.users.remove(disconnected_user)
        new_host = False
        if disconnected_user is self.host:
            new_host = True
            if len(self.users) > 0:
                self.host = self.users[0]
            else:
                self.host = None

        message_to_users = {'action': 'room', 'type': 'user_disconnect', 'user': disconnected_user,
                            'new_user_list': self.users}
        if new_host:
            message_to_users.update({'new_host': self.host})

        for user in self.users:
            user.socket.send(message_to_users)

    def update(self):
        self.quiz.update()

    def start_quiz(self):
        self.quiz.start_quiz()

    def stop_quiz(self):
        self.stop_quiz()

    def resume_quiz(self):
        self.quiz.resume_quiz()
