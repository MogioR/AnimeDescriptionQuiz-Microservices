from smart_socket import SmartSocket


class Package:
    def __init__(self, socket: SmartSocket,  message):
        self.socket = socket
        self.message = message
