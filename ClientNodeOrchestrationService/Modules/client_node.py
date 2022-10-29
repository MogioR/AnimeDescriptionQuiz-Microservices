from .smart_socket import SmartSocket


class ClientNode:
    def __init__(self, socket: SmartSocket, node_id: int, path: dict):
        self.node_id = node_id
        self.socket = socket
        self.path = path

        self.users = []

    async def add_user(self, user_id: int):
        self.users.append(user_id)
        await self.socket.send({
            'type': 'from_orchestrator',
            'data': {
                'type': 'add_user',
                'user_id': user_id
            }
        })
