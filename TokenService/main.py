import datetime
import os
import time
import json
from Modules.token_service import TokenService

from quart import Quart, request, Response

PORT = os.getenv('PORT')
AUTHENTICATION_TOKEN = os.getenv('AUTHENTICATION_TOKEN')  # APP_TOKEN
app = Quart(__name__)
token_service = TokenService()


# 9ef161e0-06bc-4692-873a-3cd91fb49c8a
# http://127.0.0.1:1234/get_token/APP_TOKEN/001
@app.route('/get_token/<string:authentication_token>/<int:userID>', methods=['GET'])
def get_token(authentication_token: str, userID: int) -> Response:
    content = request.get_json()
    print(content)

    if authentication_token == AUTHENTICATION_TOKEN:
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
def check_token(access_token: str) -> Response:
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
def refresh_token(token: str) -> Response:
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
