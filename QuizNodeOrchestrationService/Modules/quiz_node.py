from .smart_socket import SmartSocket
from .room import Room


class QuizNode:
    def __init__(self, socket: SmartSocket, node_id: int):
        self.node_id = node_id
        self.socket = socket
        self.path = str(node_id)
        self.rooms = list()

    async def create_room(self, room: Room):
        self.rooms.append(room)
        await self.socket.send({
            'type': 'from_orchestrator',
            'data': {
                'type': 'connect',
                'room_id': room.room_id,
                'room_options': room.settings
            }
        })
