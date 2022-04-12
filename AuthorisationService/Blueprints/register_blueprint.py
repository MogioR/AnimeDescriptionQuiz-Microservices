from quart import Blueprint

register_blueprint = Blueprint('/register', __name__,)


@register_blueprint.route('/register', methods=['GET'])
def register():
    print('register')
    return 'register'