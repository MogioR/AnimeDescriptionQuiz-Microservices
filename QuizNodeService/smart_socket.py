import json


class SmartSocket:
    def __init__(self, node_socket, user_id: int, message_queue: list):
        self.node_socket = node_socket
        self.user_id = user_id
        self.message_queue = message_queue

    def send(self, message: dict):
        self.message_queue.append(
            (
                self.node_socket,
                json.dumps({
                    'type': 'toUser',
                    'user': self.user_id,
                    'message': json.dumps(message)
                })
            )
        )