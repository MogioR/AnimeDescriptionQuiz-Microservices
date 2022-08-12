import asyncio
import websockets
import time
from game_node import GameNode

game_node = GameNode()


async def consumer_handler(socket):
    # while True:
    # await asyncio.sleep(0.0000000000000000001)
    async for message in socket:
        try:
            await game_node.socket_message(socket, message)
        except Exception as e:
            print("Consumer error: ", e, "socket: ", socket)


async def producer_task():
    while True:
        await asyncio.sleep(0.0000000000000000001)

        while len(game_node.message_queue) != 0:
            package = game_node.message_queue.popleft()
            try:
                await package[0].send(package[1])
            except Exception as e:
                print("Error", e)


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
    print('gg')
    connect(socket)

    consumer_task = asyncio.ensure_future(
        consumer_handler(socket)
    )
    wait_close_task = asyncio.ensure_future(
        close_handler(socket)
    )
    done, pending = await asyncio.wait(
        [consumer_task, wait_close_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


async def server_loop():
    while True:
        # print(1)
        # _old = time.time()
        await asyncio.sleep(1)
        # print(time.time() - _old)
        await game_node.update()


async def orchestrator_connect(url):
    try:
        async with websockets.connect(url) as socket:
            game_node.orchestrator_socket = socket
            await handler(socket, '')
    except Exception as e:
        print(e)

import random
port = random.randint(1000, 2000)
start_server = websockets.serve(handler, "localhost", port)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.create_task(server_loop())
loop.create_task(producer_task())
loop.create_task(orchestrator_connect('ws://127.0.0.1:1235/ws?token=API_TOKEN'))
loop.run_forever()
