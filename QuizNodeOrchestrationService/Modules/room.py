class Room:
    def __init__(self, room_id: int, settings: dict):
        self.room_id = room_id
        self.settings = settings
        self.players = []
        self.status = 'creating'
