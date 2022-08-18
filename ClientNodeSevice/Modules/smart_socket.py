import json
from collections import deque


class SmartSocket:
    def __init__(self, socket, message_queue: deque = deque()):
        self.socket = socket
        self.message_queue = message_queue

    async def send(self, message: dict, json_encoder=json.JSONEncoder):
        self.message_queue.append(
            (
                self.socket,
                json.dumps(message, cls=json_encoder, ensure_ascii=False)
            )
        )

    def __hash__(self):
        return hash(self.socket)

    def __eq__(self, other):
        return self.socket == other.node_socket
