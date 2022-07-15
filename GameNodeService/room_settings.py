class RoomSettings:
    def __init__(self, room_settings: dict):
        self.room_size = room_settings['room_size'] if 'room_size' in room_settings.keys() else 8
        self.room_name = room_settings['room_name'] if 'room_name' in room_settings.keys() else 'New room'
        self.room_protect_type = room_settings['room_protect_type'] if 'room_protect_type' in room_settings.keys() \
            else 0

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)
