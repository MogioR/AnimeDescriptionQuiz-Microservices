class ServerNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.connected_players = []

    def connected_players_count(self):
        return len(self.connected_players)
