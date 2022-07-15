from room import Room


class GameNode:
    def __init__(self):
        self.orchestrator_socket = None
        self.sockets_users = {}
        self.message_queue = []
        self.rooms = {}

    def create_room(self, room_id: int, room_settings: dict):
        self.rooms[room_id] = Room(room_settings)

    def connect_to_room(self, player_socket: int, room_id: int):
        if room_id in self.rooms.keys():
            self.rooms[room_id].connect(self.sockets_users[player_socket])
        else:
            raise Exception(f'Connect to not existing room\n'
                            f'Socket: {0}, Player: {1}, Room: {2}',
                            player_socket, self.sockets_users[player_socket], room_id)
