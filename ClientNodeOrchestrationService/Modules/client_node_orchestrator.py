import requests
from collections import deque

from .client_node import ClientNode
from .smart_socket import SmartSocket


class ClientNodeOrchestrator:
    def __init__(self):
        self.last_node_id = 0
        self.client_nodes = dict()
        self.quiz_nodes = dict()

        self.message_queue = deque()

        # self.players = dict()
        pass

    async def get_client_node(self, user_id: int):
        min_node = min(self.client_nodes.values(), key=lambda node: len(node.users))
        await min_node.add_user(user_id)
        return min_node.path

    async def connect_node(self, socket):
        self.client_nodes[SmartSocket(socket, self.message_queue)] = \
            ClientNode(SmartSocket(socket, self.message_queue), self.last_node_id, {
                'host': socket.scope['client'][0],
                'port': int(socket.headers['Port'])
            })
        self.last_node_id += 1

    async def disconnect_node(self, socket):
        del self.client_nodes[SmartSocket(socket, self.message_queue)]

    async def socket_message(self, socket, message):
        pass

    async def notify_nodes(self, message: dict):
        for node_socket in self.client_nodes.keys():
            await node_socket.send(message)

    async def add_quiz_node(self, message: dict):
        print('New quiz node:', message['node_id'], message['node_path'])
        self.quiz_nodes[message['node_id']] = message['node_path']
        await self.notify_nodes({
            'type': 'from_orchestrator',
            'data': {
                'type': 'connect_to_quiz_node',
                'node_id': message['node_id'],
                'node_path': message['node_path']
            }
        })

    async def add_quiz_nodes(self, message: dict):
        self.quiz_nodes = {a['node_id']: a['node_path'] for a in message['data']}
        await self.notify_nodes({
            'type': 'connect_to_quiz_nodes',
            'nodes': message['data']
        })

    # def check_token(self, token, node_id):
    #     response = requests.get(self.token_service_url+'/check_token/'+token)
    #     print(response.json())
    #     return self.user_in_node(response.json()['userID'], node_id)

