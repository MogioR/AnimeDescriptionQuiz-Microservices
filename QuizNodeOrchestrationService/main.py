import os
import asyncio
import json
from functools import wraps
from quart import Quart
from quart import websocket, Response, abort, request

from Modules.quiz_node_orchestrator import QuizNodeOrchestrator
from Modules.smart_socket import SmartSocket

# PORT = os.getenv('CLIENT_NODE_ORCHESTRATION_PORT')
PORT = 1235
# ws://127.0.0.1:1235/ws?token=APP_TOKEN
AUTHENTICATION_TOKEN = os.getenv('AUTHENTICATION_TOKEN')  # APP_TOKEN
app = Quart(__name__)
# node_orchestrator = NodeOrchestrator(os.getenv('TOKEN_SERVICE_HOST')+':'+os.getenv('TOKEN_SERVICE_PORT'))

PRODUCER_CREATED = False
CURRENT_SOCKET = websocket._get_current_object

quiz_node_orchestrator = QuizNodeOrchestrator()


@app.route('/create_lobby/<string:authentication_token>/<int:player_id>')
async def create_lobby(authentication_token: str, player_id: int) -> Response:
    message = await request.get_json(silent=True)
    if authentication_token == AUTHENTICATION_TOKEN:
        node_id, room_id = await quiz_node_orchestrator.create_room(message['room_options'])

        return Response(json.dumps({
            'node_id': node_id,
            'room_id': room_id
        }), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({
            'error_message': 'Incorrect token!'
        }), status=401, mimetype='application/json')


async def producer_handler():
    print(3)
    while True:
        await asyncio.sleep(0.0000000000000000001)
        while len(quiz_node_orchestrator.message_queue) != 0:
            package = quiz_node_orchestrator.message_queue.popleft()
            try:
                await package[0].send(package[1])
            except Exception as e:
                print("Error", e)


async def consumer_handler():
    while True:
        data = await websocket.receive()
        try:
            message = json.loads(data)
            await quiz_node_orchestrator.socket_message(SmartSocket(CURRENT_SOCKET()), message)
        except Exception as e:
            print(e)
            del quiz_node_orchestrator.quiz_nodes[CURRENT_SOCKET()]


def registration(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'token' in websocket.args.keys():
            if websocket.args['token'] == AUTHENTICATION_TOKEN:
                await quiz_node_orchestrator.connect_node(CURRENT_SOCKET())
                try:
                    return await func(*args, **kwargs)
                finally:
                    if SmartSocket(CURRENT_SOCKET()) not in quiz_node_orchestrator.quiz_nodes.keys():
                        await quiz_node_orchestrator.disconnect_node(CURRENT_SOCKET())

    return wrapper


@app.websocket('/ws')
@registration
async def ws():
    # ws://127.0.0.1:1235/ws?token=213123
    # print(websocket.remote_addr)
    global PRODUCER_CREATED

    while SmartSocket(CURRENT_SOCKET()) in quiz_node_orchestrator.quiz_nodes.keys():
        consumer = asyncio.create_task(consumer_handler())
        if PRODUCER_CREATED is False:
            PRODUCER_CREATED = True
            producer = asyncio.create_task(producer_handler())
            await asyncio.gather(producer, consumer)
        else:
            await asyncio.gather(consumer)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)



