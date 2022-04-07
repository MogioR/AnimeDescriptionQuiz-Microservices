import websockets
import asyncio
import json
from collections import deque


messageQueue = deque()


class ClientNode:
    sockets = dict()
    node_orchestration_socket = None
    game_nodes_sockets = dict()
    clients = dict()
    loop = None

    @staticmethod
    def start():
        start_server = websockets.serve(ClientNode.handler, "localhost", 5678)

        ClientNode.loop = asyncio.get_event_loop()
        ClientNode.loop.create_task(ClientNode.connect_to_orchestrator('ws://127.0.0.1:1235/ws?token=APP_TOKEN'))
        ClientNode.loop.run_until_complete(start_server)
        ClientNode.loop.create_task(ClientNode.producer_handler())
        ClientNode.loop.create_task(ClientNode.server_loop())
        ClientNode.loop.run_forever()

    @staticmethod
    async def connect_to_orchestrator(url):
        try:
            async with websockets.connect(url) as socket:
                ClientNode.node_orchestration_socket = socket
                while True:
                    await ClientNode.handler(socket, None)

        except Exception as e:
            print(e)

    async def connect_to_game_node(self, url):
        try:
            async with websockets.connect(url) as socket:
                ClientNode.game_nodes_sockets[socket] = 'game_node'
                while True:
                    await self.handler(socket, None)

        except Exception as e:
            print(e)

    @staticmethod
    async def handler(socket, path):
        print('handler')
        if path:
            ClientNode.sockets[socket] = 'client_node'

        consumer_task = asyncio.ensure_future(
            ClientNode.consumer_handler(socket)
        )
        wait_close_task = asyncio.ensure_future(
            ClientNode.close_handler(socket)
        )
        done, pending = await asyncio.wait(
            [consumer_task, wait_close_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

    @staticmethod
    async def consumer_handler(socket):
        async for message in socket:
            print(socket, message)
            try:
                await ClientNode.consumer(socket, message)
            except Exception as e:
                print("Consumer error: ", e, "socket: ", socket)

    @staticmethod
    async def producer_handler():
        while True:
            while len(messageQueue) != 0:
                print('d')
                package = messageQueue.popleft()
                print(package.socket, package.message)
                try:
                    await package.socket.send(package.message)
                except Exception as e:
                    print("Error", e)

            await asyncio.sleep(0.1)

    @staticmethod
    async def close_handler(socket):
        await socket.wait_closed()
        # disconnect(socket)

    @staticmethod
    async def consumer(socket, message):
        print(message)

    @staticmethod
    async def server_loop():
        while True:
            print(1)
            await asyncio.sleep(1)
