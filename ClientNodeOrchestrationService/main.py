import os
import asyncio
import json
from functools import wraps
from quart import Quart
from quart import websocket, Response, abort
from Modules.node_orchestrator import NodeOrchestrator

PORT = os.getenv('CLIENT_NODE_ORCHESTRATION_PORT')
# ws://127.0.0.1:1235/ws?token=APP_TOKEN
AUTHENTICATION_TOKEN = os.getenv('AUTHENTICATION_TOKEN')  # APP_TOKEN
app = Quart(__name__)
node_orchestrator = NodeOrchestrator(os.getenv('TOKEN_SERVICE_HOST')+':'+os.getenv('TOKEN_SERVICE_PORT'))

message_queue = []
connected_sockets = dict()


@app.route('/get_node/<string:authentication_token>/<int:player_id>')
async def get_node(authentication_token: str, player_id: int) -> Response:
    if authentication_token == AUTHENTICATION_TOKEN:
        return Response(json.dumps({
            'nodeId': node_orchestrator.get_server_node(player_id)
        }), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({
            'errorMessage': 'Incorrect token!'
        }), status=401, mimetype='application/json')


async def sending():
    if len(message_queue) > 0:
        await websocket.send('f{1}')
    await asyncio.sleep(1)


async def receiving():
    data = await websocket.receive()
    try:
        lol = json.loads(data)
        print(lol)
    except:
        print('gg')
        del connected_sockets[websocket._get_current_object()]


def registration(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global connected_sockets
        if 'token' in websocket.args.keys():
            if websocket.args['token'] == AUTHENTICATION_TOKEN:
                connected_sockets[websocket._get_current_object()] = len(connected_sockets)
                node_orchestrator.add_server_node(websocket._get_current_object())
                try:
                    return await func(*args, **kwargs)
                finally:
                    if websocket._get_current_object() in connected_sockets.keys():
                        del connected_sockets[websocket._get_current_object()]

    return wrapper


@app.websocket('/ws')
@registration
async def ws():
    # ws://127.0.0.1:1235/ws?token=213123
    # print(websocket.remote_addr)
    print(len(connected_sockets))
    print(websocket.args)
    # print(websocket.authorization)
    while websocket._get_current_object() in connected_sockets.keys():
        producer = asyncio.create_task(sending())
        consumer = asyncio.create_task(receiving())
        await asyncio.gather(producer, consumer)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)

