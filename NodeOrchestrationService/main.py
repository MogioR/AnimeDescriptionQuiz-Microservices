import os
import asyncio
from quart import Quart
from quart import websocket
from Modules.node_orchestrator import NodeOrchestrator

AUTHENTICATION_TOKEN = os.getenv('AUTHENTICATION_TOKEN')  # ya_ebal_sobaky
app = Quart(__name__)
node_orchestrator = NodeOrchestrator('localhost')

message_queue = []

@app.route('/get_node/<string:authentication_token>/<int:player_id>')
async def get_node(authentication_token: str, player_id: int) -> str:
    if authentication_token == AUTHENTICATION_TOKEN:
        return str({
            'statusCode': 200,
            'nodeId': node_orchestrator.get_server_node(player_id)
        })
    else:
        return str({
            'statusCode': 401,
            'errorMessage': 'Incorrect authentication token!'
        })


async def check_token():
    pass


async def sending():
    while True:
        if len(message_queue) > 0:
            await websocket.send('f{1}')
        await asyncio.sleep(1)


async def receiving():
    while True:
        data = await websocket.receive()
        if data == 'lol':
            print(connected[websocket])
        print(data + "\n=====")


from functools import wraps
from secrets import compare_digest
connected = dict()


def collect_websocket(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global connected
        connected[websocket._get_current_object()] = len(connected)
        try:
            return await func(*args, **kwargs)
        finally:
            del connected[websocket._get_current_object()]
    return wrapper


lol = set()
@app.websocket('/ws')
@collect_websocket
async def ws():
    # print(websocket.remote_addr)
    print(len(connected))
    while True:
        producer = asyncio.create_task(sending())
        consumer = asyncio.create_task(receiving())
        await asyncio.gather(producer, consumer)


if __name__ == '__main__':
    app.run(debug=True)
