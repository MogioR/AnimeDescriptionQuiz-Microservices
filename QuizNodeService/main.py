import asyncio
import websockets
import socket
import os
from QuizNodeService.Modules.game_node import GameNode

game_node = GameNode()


async def producer_task():
    while True:
        await asyncio.sleep(0.0000000000000000001)

        while len(game_node.message_queue) != 0:
            package = game_node.message_queue.popleft()
            try:
                await package[0].send(package[1])
            except Exception as e:
                print("Error", e)


async def consumer_handler(socket):
    try:
        async for message in socket:
            try:
                await game_node.socket_message(socket, message)
            except Exception as e:
                print("Consumer error: ", e, "socket: ", socket)
    except Exception as e:
        print(e)


async def close_handler(websocket):
    await websocket.wait_closed()
    disconnect(websocket)


def connect(socket: websockets):
    if game_node.orchestrator_socket is None:
        game_node.orchestrator_socket = socket
    else:
        game_node.node_sockets.add(socket)
    print(socket, 'CONNECTED')


def disconnect(socket: websockets):
    if game_node.orchestrator_socket == socket:
        game_node.orchestrator_socket = None
    else:
        game_node.node_sockets.discard(socket)
    print(socket, 'DISCONNECTED')


async def handler(socket, path):
    connect(socket)

    consumer_task = asyncio.ensure_future(
        consumer_handler(socket)
    )
    wait_close_task = asyncio.ensure_future(
        close_handler(socket)
    )
    done, pending = await asyncio.wait(
        [wait_close_task, consumer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


async def server_loop():
    while True:
        await asyncio.sleep(1)
        await game_node.update()


async def web_socket_connect(url):
    try:
        async with websockets.connect(url, extra_headers={'port': game_node.port}) as socket:
            await handler(socket, '')
    except Exception as e:
        print(e)


start_server = websockets.serve(handler, "localhost", port=None, family=socket.AF_INET)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.create_task(server_loop())
game_node.port = start_server.ws_server.server.sockets[0].getsockname()[1]
loop.create_task(producer_task())
loop.create_task(web_socket_connect(
    'ws://' + os.getenv('QUIZ_NODE_ORCHESTRATION_HOST') +
    ':' + os.getenv('QUIZ_NODE_ORCHESTRATION_PORT') + '/ws?token=' +
    os.getenv('AUTHENTICATION_TOKEN')
))
loop.run_forever()
