import asyncio
import websockets
from game_node import GameNode

game_node = GameNode()


async def consumer_handler(socket, path):
    async for message in socket:
        try:
            await game_node.socket_message(socket, message)
        except Exception as e:
            print("Consumer error: ", e, "socket: ", socket)


async def producer_handler():
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


def disconnect(socket: websockets):
    if game_node.orchestrator_socket == socket:
        game_node.orchestrator_socket = None
    else:
        game_node.orchestrator_socket.discard(socket)
    print(socket, 'DISCONNECTED')


async def handler(socket, path):
    connect(socket)

    consumer_task = asyncio.ensure_future(
        consumer_handler(socket, path)
    )
    producer_task = asyncio.ensure_future(
        producer_handler()
    )
    wait_close_task = asyncio.ensure_future(
        close_handler(socket)
    )
    done, pending = await asyncio.wait(
        [consumer_task, producer_task, wait_close_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


async def server_loop():
    while True:
        print(1)
        await game_node.update()


start_server = websockets.serve(handler, "localhost", 5677)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
