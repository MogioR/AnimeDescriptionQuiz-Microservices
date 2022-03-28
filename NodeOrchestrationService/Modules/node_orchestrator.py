import requests
from .server_node import ServerNode


class NodeOrchestrator:
    def __init__(self, token_service_url: str):
        self.token_service_url = token_service_url
        self.server_nodes = dict()
        self.count_of_nodes = 0

    def add_server_node(self, socket):
        self.server_nodes[socket] = ServerNode(self.count_of_nodes)
        self.count_of_nodes += 1

    def get_server_node(self, player_id):
        min_socket = 0
        for socket in self.server_nodes.keys():
            if self.server_nodes[socket].connected_players_count() < self.server_nodes[min_socket]:
                min_socket = socket

        self.server_nodes[min_socket].connected_players += player_id
        return self.server_nodes[min_socket].node_id

    def check_token(self, token, node_id):
        response = requests.get(self.token_service_url+'/check_token/'+token)

        print(response.json())
        return self.user_in_node(response.json()['userID'], node_id)

    def user_in_node(self, user_id, node_id):
        for node in self.server_nodes:
            if node.node_id == node_id:
                return user_id in node.connected_players
        return False
