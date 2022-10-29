import os
import asyncio
import json
from functools import wraps
from quart import Quart
from quart import websocket, Response, abort, request

from Modules.client_node_orchestrator import ClientNodeOrchestrator
from Modules.smart_socket import SmartSocket

PORT = os.getenv('CLIENT_NODE_ORCHESTRATION_PORT')
AUTHENTICATION_TOKEN = os.getenv('AUTHENTICATION_TOKEN')
app = Quart(__name__)

PRODUCER_CREATED = False
CURRENT_SOCKET = websocket._get_current_object

client_node_orchestrator = ClientNodeOrchestrator()


@app.route('/get_node/<string:authentication_token>/<int:player_id>')
async def get_node(authentication_token: str, player_id: int) -> Response:
    if authentication_token == AUTHENTICATION_TOKEN:
        node_path = await client_node_orchestrator.get_client_node(player_id)
        return Response(json.dumps({
            'nodePath': node_path
        }), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({
            'errorMessage': 'Incorrect token!'
        }), status=401, mimetype='application/json')


@app.route('/add_quiz_node/<string:authentication_token>/')
async def add_quiz_node(authentication_token: str) -> Response:
    message = await request.get_json(silent=True)
    if authentication_token == AUTHENTICATION_TOKEN:
        await client_node_orchestrator.add_quiz_node(message)
        return Response('ok', status=200, mimetype='application/json')
    else:
        return Response(json.dumps({
            'errorMessage': 'Incorrect token!'
        }), status=401, mimetype='application/json')


@app.route('/add_quiz_nodes/<string:authentication_token>/')
async def add_quiz_nodes(authentication_token: str) -> Response:
    message = await request.get_json(silent=True)
    if authentication_token == AUTHENTICATION_TOKEN:
        await client_node_orchestrator.add_quiz_nodes(message)
        return Response('ok', status=200, mimetype='application/json')
    else:
        return Response(json.dumps({
            'errorMessage': 'Incorrect token!'
        }), status=401, mimetype='application/json')


async def producer_handler():
    while True:
        await asyncio.sleep(0.0000000000000000001)
        while len(client_node_orchestrator.message_queue) != 0:
            package = client_node_orchestrator.message_queue.popleft()
            try:
                await package[0].send(package[1])
            except Exception as e:
                print("Error", e)


async def consumer_handler():
    while True:
        data = await websocket.receive()
        try:
            message = json.loads(data)
            await client_node_orchestrator.socket_message(SmartSocket(CURRENT_SOCKET()), message)
        except Exception as e:
            print(e)
            del client_node_orchestrator.client_nodes[CURRENT_SOCKET()]


def registration(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'token' in websocket.args.keys():
            if websocket.args['token'] == AUTHENTICATION_TOKEN:
                await client_node_orchestrator.connect_node(CURRENT_SOCKET())
                try:
                    return await func(*args, **kwargs)
                finally:
                    if SmartSocket(CURRENT_SOCKET()) not in client_node_orchestrator.client_nodes.keys():
                        await client_node_orchestrator.disconnect_node(CURRENT_SOCKET())

    return wrapper


@app.websocket('/ws')
@registration
async def ws():
    global PRODUCER_CREATED

    while SmartSocket(CURRENT_SOCKET()) in client_node_orchestrator.client_nodes.keys():
        consumer = asyncio.create_task(consumer_handler())
        if PRODUCER_CREATED is False:
            PRODUCER_CREATED = True
            producer = asyncio.create_task(producer_handler())
            await asyncio.gather(producer, consumer)
        else:
            await asyncio.gather(consumer)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
