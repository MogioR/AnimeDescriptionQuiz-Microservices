import asyncio
import websockets
import os
import json

from .Modules.client_node import ClientNode
from .Modules.smart_socket import SmartSocket

client_node = ClientNode()


async def producer_task():
    while True:
        await asyncio.sleep(0.0000000000000000001)

        while len(client_node.message_queue) != 0:
            package = client_node.message_queue.popleft()
            try:
                await package[0].send(package[1])
            except Exception as e:
                print("Error", e)


async def consumer_handler(socket):
    async for message in socket:
        try:
            message = json.loads(message)
            await client_node.socket_message(socket, message)
        except Exception as e:
            print("Consumer error: ", e, "socket: ", socket)


async def close_handler(websocket):
    await websocket.wait_closed()
    disconnect(websocket)


def user_connect(socket: websockets, context):
    if 'user_id' in socket.request_headers.keys():
        client_node.connect_to_quiz_node(
            SmartSocket(socket, client_node.message_queue),
            socket.request_headers['user_id']
        )
        print(socket, socket.request_headers['user_id'], 'CONNECTED')


def orchestrator_connect(socket: websockets, context):
    client_node.orchestrator_socket = socket


def quiz_node_connect(socket: websockets, context):
    client_node.connect_to_quiz_node(socket, context['node_id'])


def disconnect(socket: websockets):
    if client_node.orchestrator_socket == socket:
        client_node.orchestrator_socket = None
    else:
        client_node.disconnect_from_quiz_node(SmartSocket(socket, client_node.message_queue))
    print(socket, 'DISCONNECTED')


async def handler(socket, path, connect_func=user_connect, context=None):
    connect_func(socket, context)

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


async def web_socket_connect(url, connect_func, context=None):
    try:
        async with websockets.connect(url) as socket:
            await handler(socket, '', connect_func=connect_func, context=context)
    except Exception as e:
        print(e)


async def connect_to_quiz_node(node_path, node_id):
    loop.create_task(web_socket_connect(
        'ws://' + node_path['host'] +
        ':' + node_path['port'] + '/ws?token=' +
        os.getenv('AUTHENTICATION_TOKEN'),
        quiz_node_connect,
        {'node_id': node_id}
    ))

client_node.connect_node_func = connect_to_quiz_node

start_server = websockets.serve(handler, "localhost", None)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.create_task(producer_task())
loop.create_task(web_socket_connect(
    'ws://' + os.getenv('CLIENT_NODE_ORCHESTRATION_HOST') +
    ':' + os.getenv('CLIENT_NODE_ORCHESTRATION_PORT') + '/ws?token=' +
    os.getenv('AUTHENTICATION_TOKEN'),
    orchestrator_connect
))
loop.run_forever()
