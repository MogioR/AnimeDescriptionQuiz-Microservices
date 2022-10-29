import asyncio
import requests
import os
from collections import deque

from .quiz_node import QuizNode
from .smart_socket import SmartSocket
from .room import Room


class QuizNodeOrchestrator:
    def __init__(self):
        self.last_node_id = 0
        self.last_room_id = 0
        self.quiz_nodes = dict()
        self.message_queue = deque()

        self.rooms = dict()
        # self.players = dict()

    async def connect_node(self, socket):
        self.quiz_nodes[SmartSocket(socket, self.message_queue)] = \
            QuizNode(SmartSocket(socket, self.message_queue), self.last_node_id, {
                'host': socket.scope['client'][0],
                'port': int(socket.headers['Port'])
            })
        lol = requests.post(
            url='http://' + os.getenv('CLIENT_NODE_ORCHESTRATION_HOST') + ':' + os.getenv(
                'CLIENT_NODE_ORCHESTRATION_PORT') + '/add_quiz_node/'+os.getenv('AUTHENTICATION_TOKEN'),
            data={
                'node_id': self.last_node_id,
                'node_path': {
                    'host': socket.scope['client'][0],
                    'port': int(socket.headers['Port'])
                }
            }
        )
        self.last_node_id += 1

    async def disconnect_node(self, socket):
        del self.quiz_nodes[SmartSocket(socket, self.message_queue)]

    async def create_room(self, settings: dict):
        room_id = self.last_room_id
        self.last_room_id += 1

        self.rooms[room_id] = Room(room_id, settings)
        min_quiz_node = min(self.quiz_nodes.values(), key=lambda node: len(node.rooms))
        await min_quiz_node.create_room(self.rooms[room_id])

        await self.room_created_trigger(room_id)
        return min_quiz_node.node_id, room_id

    async def room_created_trigger(self, room_id):
        while self.rooms[room_id].status == 'creating':
            await asyncio.sleep(0.0000000000000000001)

    async def get_room_list(self):
        return self.rooms

    async def room_created(self, room_id):
        print('Room created log')
        self.rooms[room_id].status = 'inRoom'

    async def room_closed(self, room_id):
        del self.rooms[room_id]

    async def room_update(self, room_id, message):
        if message['type'] == 'connect_player':
            self.rooms[room_id].players.append(message['player_id'])
        elif message['type'] == 'disconnect_player':
            self.rooms[room_id].players.remove(message['player_id'])
        elif message['type'] == 'update_state':
            self.rooms[room_id].status = message['status']
        elif message['type'] == 'update_settings':
            self.rooms[room_id].settings = message['update_settings']

    async def socket_message(self, socket, message):
        try:
            if message['type'] == 'room_created':
                await self.room_created(message['room_id'])
            elif message['type'] == 'room_closed':
                await self.room_closed(message['room_id'])
            elif message['type'] == 'room_update':
                await self.room_update(message['room_id'], message['message'])
        except Exception as e:
            print(e)

    # def player_update(self):
    #     pass
