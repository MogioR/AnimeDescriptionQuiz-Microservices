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
    messageQueue.append(Package(socket, '{}'))


async def consumer_handler(socket, path):
    async for message in socket:
        print(socket, message)
        try:
            await consumer(socket, message)
        except Exception as e:
            print("Consumer error: ", e, "socket: ", socket)


async def producer_handler():
    while len(messageQueue) != 0:
        print('d')
        package = messageQueue.popleft()
        print(package.socket, package.message)
        try:
            await package.socket.send(package.message)
        except Exception as e:
            print("Error", e)


async def close_handler(websocket):
    await websocket.wait_closed()
    disconnect(websocket)


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
        await asyncio.sleep(1)

start_server = websockets.serve(handler, "localhost", 5677)


loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
