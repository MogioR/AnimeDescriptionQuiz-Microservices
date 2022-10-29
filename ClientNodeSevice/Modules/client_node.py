from collections import deque


from .smart_socket import SmartSocket
from .smart_dict import SmartDict


class ClientNode:
    def __init__(self):
        self.orchestrator_socket = None
        self.connect_node_func = None
        self.port = None

        self.message_queue = deque()
        self.nodes = SmartDict()
        self.users = SmartDict()

        self.allowed_users = list()

    def user_connect(self, socket: SmartSocket, user_id):
        # self.allowed_users.remove(user_id)
        self.users.set(socket, user_id)

    def user_disconnect(self, socket: SmartSocket):
        self.users.del_by_key(socket)

    async def socket_message(self, socket: SmartSocket, message: dict):
        if socket in self.users.keys():
            await self.user_message(socket, message)
        elif socket in self.nodes.keys():
            await self.quiz_node_message(socket, message)
        else:
            await self.orchestrator_message(message)

    async def user_message(self, socket, message: dict):
        if message['type'] == 'toQuizNode':
            if message['quiz_node'] in self.nodes.values():
                self.nodes.get_by_value(message['quiz_node']).send(message['message'])

    async def quiz_node_message(self, socket, message: dict):
        if message['type'] == 'toUser':
            if message['user'] in self.users.values():
                self.users.get_by_value(message['user']).send(message['message'])

    async def orchestrator_message(self, message):
        message = message['data']
        if message['type'] == 'add_user':
            self.allowed_users.append(message['user_id'])
        elif message['type'] == 'connect_to_quiz_node':
            print('New quiz node:', message['node_id'], message['node_path'])
            await self.connect_node_func(message['node_path'], message['node_id'])
        elif message['type'] == 'connect_to_quiz_nodes':
            async for context in message['nodes']:
                await self.connect_node_func(context['node_path'], context['node_id'])

    def quiz_node_connect(self, socket: SmartSocket, node_id: int):
        self.nodes.set(socket, node_id)

    def quiz_node_disconnect(self, socket):
        self.nodes.del_by_key(socket)
