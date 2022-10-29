import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '_Models')

import json
import requests

from _Models.user_model import UserModel
from quart import Blueprint, request, Response

login_blueprint = Blueprint('/login', __name__, )

token_headers = {
    'user-agent': 'authorisation_service 0.1',
    'Access-Token': os.getenv('AUTHENTICATION_TOKEN')
}


@login_blueprint.route('/login', methods=['GET'])
async def login():
    print(request.is_json)
    message = await request.get_json(silent=True)
    if message is not None:
        if 'login' in message.keys() and 'password' in message.keys():
            password_hash = message['password']

            try:
                user = UserModel.get(
                    UserModel.user_login == message['login'],
                    UserModel.user_pass_hash == password_hash
                )
            except Exception as e:
                print(e)
                user = None

            if user is not None:
                print(user.user_id)
                # Get token
                token = requests.get(
                    url='http://' + os.getenv('TOKEN_SERVICE_HOST') + ':' + os.getenv(
                        'TOKEN_SERVICE_PORT') + '/get_token/1',
                    headers=token_headers
                )
                # Get client node
                node_id = requests.get(
                    url='http://' + os.getenv('CLIENT_NODE_ORCHESTRATION_HOST') + ':' \
                        + os.getenv('CLIENT_NODE_ORCHESTRATION_PORT') + '/get_node/' \
                        + os.getenv('AUTHENTICATION_TOKEN') + '/' + str(user.user_id),
                    headers=token_headers
                )
                return Response(json.dumps({
                        'token': token.json(),
                        'node_path': node_id.json()
                    }), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({
                    'error': 'Invalid login or password!'
                }), status=403, mimetype='application/json')
        else:
            return Response(json.dumps({
                'error': 'Bad json struct!',
            }), status=400, mimetype='application/json')
    else:
        return Response(json.dumps({
            'error': 'Error parse JSON!',
        }), status=400, mimetype='application/json')
