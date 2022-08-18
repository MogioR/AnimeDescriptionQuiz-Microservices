import json
from collections import deque


class SmartSocket:
    def __init__(self, node_socket, user_id: int, message_queue: deque):
        self.node_socket = node_socket
        self.user_id = user_id
        self.message_queue = message_queue

    async def send(self, message: dict, json_encoder=json.JSONEncoder):
        self.message_queue.append(
            (
                self.node_socket,
                json.dumps({
                    'type': 'toUser',
                    'user': self.user_id,
                    'message': message
                }, cls=json_encoder, ensure_ascii=False)
            )
        )

    def __hash__(self):
        return hash((self.node_socket, self.user_id))

    def __eq__(self, other):
        return (self.node_socket, self.user_id) == (other.node_socket, other.user_id)
