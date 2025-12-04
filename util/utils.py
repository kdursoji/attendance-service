# project/api/utils.py


from functools import wraps

from flask import request, jsonify

from datastore.deps import session_scope
from models.users import User
from util.ignore_requests import check_ignore_token


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if check_ignore_token(request.path, request.method):
            return

        response_object = {
            'status': 'error',
            'message': 'Something went wrong. Please contact us.'
        }
        code = 401
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response_object['message'] = 'Provide a valid auth token.'
            code = 403
            return jsonify(response_object), code
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)

        if isinstance(resp, str):
            response_object['message'] = resp
            return jsonify(response_object), code

        with session_scope() as session:
            import crud
            user = crud.user_crud_handler.get_row_by_user_id(db=session, id=resp)
            http_args = request.args.to_dict()
            http_args['userId'] = user.id
            from starlette.datastructures import ImmutableMultiDict
            request.args = ImmutableMultiDict(http_args)

        return f(*args, **kwargs)

    return decorated_function


def is_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.admin
