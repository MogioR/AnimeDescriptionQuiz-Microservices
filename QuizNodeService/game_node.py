import asyncio
import json
import os
import sys
from collections import deque

from room import Room
from user import User
from smart_socket import SmartSocket

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '\\_Shared_modules')

from _Shared_modules._Models import UserModel, UserStatsModel


class GameNode:
    def __init__(self):
        self.orchestrator_socket = None
        self.node_sockets = set()

        self.sockets_users = {}
        self.message_queue = deque()
        self.rooms = {}

    async def create_room(self, room_id: int, room_settings: dict):
        print('Room created')
        self.rooms[room_id] = Room(room_settings)

    async def connect_to_room(self, smart_socket: SmartSocket, room_id: int):
        print('Connected to room')
        if room_id in self.rooms.keys():
            user_data = await self.get_user_data(smart_socket.user_id)
            self.sockets_users[smart_socket] = User(smart_socket, user_data)

            is_connected = await self.rooms[room_id].connect(self.sockets_users[smart_socket])
            if is_connected:
                self.sockets_users[smart_socket].room = room_id
            else:
                del self.sockets_users[smart_socket]
        else:
            raise Exception(f'Connect to not existing room\n'
                            f'Socket: {0}, Player: {1}, Room: {2}',
                            smart_socket.node_socket, self.sockets_users[smart_socket], room_id)

    @staticmethod
    async def get_user_data(user_id: int) -> dict:
        u = UserModel.select(UserModel, UserStatsModel).where(UserModel.user_id == user_id).join(UserStatsModel).get()
        return {
            'username': u.user_login,
            'experience': u.userstatsmodel.user_stats_exp
        }

    async def disconnect_from_room(self, smart_socket):
        print('Disconnected to room')
        if self.sockets_users[smart_socket].room == -1:
            del self.sockets_users[smart_socket]
        else:
            await self.rooms[self.sockets_users[smart_socket].room].disconnect()
            del self.sockets_users[smart_socket]

    async def socket_message(self, socket, message):
        try:
            message = json.loads(message)
            if socket == self.orchestrator_socket:
                if message['type'] == 'from_orchestrator':
                    await self.create_room(message['room_id'], message['room_options'])
            else:
                if message['type'] == 'from_user':
                    message = message['data']
                    if message['type'] == 'connect':
                        await self.connect_to_room(
                            SmartSocket(socket, message['from_user'], self.message_queue),
                            message['room_id']
                        )
                    elif message['type'] == 'disconnect':
                        await self.disconnect_from_room(
                            SmartSocket(socket, message['from_user'], self.message_queue)
                        )
                    elif message['type'] == 'send_to_room':
                        await self.rooms[
                            self.sockets_users[SmartSocket(socket, message['from_user'], self.message_queue)].room
                        ].message_produce(message['from_user'], message['data'])

        except Exception as e:
            print(e)

    async def update(self):
        for room in self.rooms.values():
            await room.update()
    # def connect(self, socket, user_id, message_queue):
    #     smart_socket = SmartSocket(socket, user_id, message_queue)
    #     self.sockets_users[smart_socket] = User(smart_socket, user_id, {})
