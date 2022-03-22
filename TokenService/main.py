import datetime
import os
import time

from Modules.token_service import TokenService

from flask import Flask


AUTHENTICATION_TOKEN = os.getenv('AUTHENTICATION_TOKEN')  # ya_ebal_sobaky
app = Flask(__name__)
token_service = TokenService()


@app.route('/get_token/<string:authentication_token>/<int:userID>', methods=['GET'])
def get_token(authentication_token: str, userID: int) -> str:
    if authentication_token == AUTHENTICATION_TOKEN:
        token = token_service.create_token(userID)
        return str({
            'statusCode': 200,
            'access_token': token.access_token,
            'refresh_token': token.refresh_token,
            'expiresTime': int(token.expires_time)
        })
    else:
        return str({
            'statusCode': 401,
            'errorMessage': 'Incorrect authentication token!'
        })


@app.route('/check_token/<string:access_token>', methods=['GET'])
def check_token(access_token: str) -> str:
    data, expire = token_service.check_token(access_token)
    if data is not None:
        if not expire:
            return str({
                'statusCode': 200,
                'userID': data
            })
        return str({
            'statusCode': 400,
            'errorMessage': 'Token has expire!'
        })
    else:
        return str({
            'statusCode': 400,
            'errorMessage': 'Incorrect token!'
        })


@app.route('/refresh_token/<string:refresh_token>', methods=['GET'])
def refresh_token(refresh_token: str) -> str:
    token = token_service.refresh_token(refresh_token)
    if token is not None:
        return str({
            'statusCode': 200,
            'access_token': token.access_token,
            'refresh_token': token.refresh_token,
            'expiresTime': int(token.expires_time)
        })
    else:
        return str({
            'statusCode': 401,
            'errorMessage': 'Incorrect refresh token!'
        })


if __name__ == '__main__':
    app.run(debug=True)
