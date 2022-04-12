import datetime
import os
import time
import json
from Modules.token_service import TokenService

from quart import Quart, request, Response

PORT = os.getenv('TOKEN_SERVICE_PORT')
AUTHENTICATION_TOKEN = os.getenv('AUTHENTICATION_TOKEN')  # APP_TOKEN
app = Quart(__name__)
token_service = TokenService()


# http://127.0.0.1:1234/get_token/001
@app.route('/get_token/<int:userID>', methods=['GET'])
async def get_token(userID: int) -> Response:
    if 'Access-Token' in request.headers.keys() and request.headers['Access-Token'] == AUTHENTICATION_TOKEN:
        token = token_service.create_token(userID)
        return Response(json.dumps({
            'access_token': token.access_token,
            'refresh_token': token.refresh_token,
            'expiresTime': int(token.expires_time)
        }), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({
            'errorMessage': 'Incorrect token!'
        }), status=401, mimetype='application/json')


@app.route('/check_token/<string:access_token>', methods=['GET'])
async def check_token(access_token: str) -> Response:
    data, expire = token_service.check_token(access_token)
    if data is not None:
        if not expire:
            return Response(json.dumps({
                'statusCode': 200,
                'userID': data
            }), status=200, mimetype='application/json')
        return Response(json.dumps({
            'errorMessage': 'Token has expire!'
        }), status=401, mimetype='application/json')
    else:
        return Response(json.dumps({
            'errorMessage': 'Incorrect token!'
        }), status=401, mimetype='application/json')


@app.route('/refresh_token/<string:token>', methods=['GET'])
async def refresh_token(token: str) -> Response:
    token = token_service.refresh_token(token)
    if token is not None:
        return Response(json.dumps({
            'statusCode': 200,
            'access_token': token.access_token,
            'refresh_token': token.refresh_token,
            'expiresTime': int(token.expires_time)
        }), status=200, mimetype='application/json')

    else:
        return Response(json.dumps({
            'errorMessage': 'Incorrect refresh token!'
        }), status=401, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
