import datetime
import os
import time
import json
from quart import Quart, request, Response
from Blueprints.login_blueprint import login_blueprint
from Blueprints.register_blueprint import register_blueprint

PORT = os.getenv('PORT')
AUTHENTICATION_TOKEN = os.getenv('AUTHENTICATION_TOKEN')  # APP_TOKEN
app = Quart(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)


@app.errorhandler
def default_error_handler(err):
    return {"errors": {"message": str(err)}}, getattr(err, "code", 500)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)