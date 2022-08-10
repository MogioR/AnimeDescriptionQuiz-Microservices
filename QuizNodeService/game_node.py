import asyncio
from collections import deque

from .room import Room
from .user import User
from .smart_socket import SmartSocket


class GameNode:
    def __init__(self):
        self.orchestrator_socket = None
        self.node_sockets = set()

        self.sockets_users = {}
        self.message_queue = deque()
        self.rooms = {}

    async def create_room(self, room_id: int, room_settings: dict):
        self.rooms[room_id] = Room(room_settings)

    async def connect_to_room(self, smart_socket: SmartSocket, room_id: int):
        if room_id in self.rooms.keys():
            is_connected = await self.rooms[room_id].connect(self.sockets_users[smart_socket])
            if not is_connected:
                del self.sockets_users[smart_socket]
        else:
            raise Exception(f'Connect to not existing room\n'
                            f'Socket: {0}, Player: {1}, Room: {2}',
                            smart_socket.node_socket, self.sockets_users[smart_socket], room_id)

    async def disconnect_from_room(self, smart_socket):
        if self.sockets_users[smart_socket].room == -1:
            del self.sockets_users[smart_socket]
        else:
            await self.rooms[self.sockets_users[smart_socket].room].disconnect()
            del self.sockets_users[smart_socket]

    async def socket_message(self, socket, message):
        try:
            if socket == self.orchestrator_socket:
                if message['type'] == 'new_room':
                    await self.create_room(message['room_id'], message['room_options'])
            else:
                if message['type'] == 'toNode':
                    message = message['data']
                    if message['type'] == 'connect':
                        await self.connect_to_room(
                            SmartSocket(socket, message['fromUser'], self.message_queue),
                            message['room_id']
                        )
                    elif message['type'] == 'disconnect':
                        await self.disconnect_from_room(
                            SmartSocket(socket, message['fromUser'], self.message_queue)
                        )
                elif message['type'] == 'toRoom':
                    await self.rooms[
                        self.sockets_users[SmartSocket(socket, message['fromUser'], self.message_queue)]
                    ].message_produce(message['fromUser'], message['data'])

        except Exception as e:
            print(e)

    async def update(self):
        for room in self.rooms:
            await room.update()
    # def connect(self, socket, user_id, message_queue):
    #     smart_socket = SmartSocket(socket, user_id, message_queue)
    #     self.sockets_users[smart_socket] = User(smart_socket, user_id, {})
