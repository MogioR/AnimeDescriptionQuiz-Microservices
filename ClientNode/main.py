import asyncio
import websockets
from collections import deque
import json
import threading

import requests
import re

messageQueue = deque()
gameLoopAlive = 0

clients_id_to_socket = {}
clients_socket_to_id = {}


async def consumer(socket, message):
    print(message)


async def consumer_handler(socket):
    async for message in socket:
        print(socket, message)
        try:
            await consumer(socket, message)
        except Exception as e:
            print("Consumer error: ", e, "socket: ", socket)


async def producer_handler():
    while True:
        await asyncio.sleep(0.1)
        while len(messageQueue) != 0:
            package = messageQueue.popleft()
            print(package.socket, package.message)
            try:
                await package.socket.send(package.message)
            except Exception as e:
                print("Error", e)

async def close_handler(socket):
    await socket.wait_closed()
    disconnect(socket)


def connect(socket: websockets):
    len_ = len(clients_id_to_socket)
    clients_id_to_socket[len_] = socket
    clients_socket_to_id[socket] = len_
    print(socket, 'CONNECTED')


def disconnect(socket: websockets):
    id_ = clients_socket_to_id[socket]
    del clients_id_to_socket[id_]
    del clients_socket_to_id[socket]
    print(socket, 'DISCONNECTED')


async def handler(socket, path):
    connect(socket)

    consumer_task = asyncio.ensure_future(
        consumer_handler(socket)
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
        await asyncio.sleep(1)


message_queue = []
websocketss = []


async def sending(websocket):
    if len(message_queue) > 0:
        await websocket.send('f{1}')
    await asyncio.sleep(1)


async def receiving(websocket):
    data = await websocket.recv()
    try:
        lol = json.loads(data)
        print(lol)
    except:
        print('gg')


async def websocket_connect(url):
    try:
        async with websockets.connect(url) as websocket:
            websocketss.append(websocket)
            print(websocketss)
            while True:
                consumer_task = asyncio.ensure_future(
                    receiving(websocket)
                )
                producer_task = asyncio.ensure_future(
                    sending(websocket)
                )
                done, pending = await asyncio.wait(
                    [consumer_task, producer_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                for task in pending:
                    task.cancel()
    except Exception as e:
        print(e)


# start_server = websockets.serve(handler, "localhost", 5678)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(start_server)
# loop.create_task(websocket_connect('ws://127.0.0.1:1235/ws?token=APP_TOKEN'))
# loop.create_task(websocket_connect('ws://127.0.0.1:1235/ws?token=APP_TOKEN'))
# loop.run_forever()

from Modules.socket_maneger import ClientNode

ClientNode.start()
