# project/__init__.py
import json
import os
from datetime import datetime
from traceback import print_exc

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from util.dt_encoder import DTEncoder
from util.ignore_requests import check_ignore_token

# instantiate the extensions

bcrypt = Bcrypt()


def create_app(config_name):
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    app.config.from_object(load_config())

    bcrypt.init_app(app)

    # Register REST API blueprints - separate modules for each resource
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    from app.api.organizations import organizations_bp
    from app.api.attendance import attendance_bp

    # Register blueprints with /api prefix
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(organizations_bp, url_prefix='/api')
    app.register_blueprint(attendance_bp, url_prefix='/api')

    # Register global exception handlers
    from exceptions.exception_handlers import register_exception_handlers
    register_exception_handlers(app)

    from util.utils import authenticate
    @app.before_request
    #@authenticate
    def verify_token():
        pass

    @app.after_request
    def after_request(response):
        from flask import request
        if check_ignore_token(request.path, request.method):
            return response

        now = datetime.now()  # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        user_activity = {
            "service_name": "localite-user-service",
            "request_remote_address": request.remote_addr,
            "request_time": date_time,
            "request_method_type": request.method,
            "request_path": request.path,
            "request_schema": request.scheme,
            "response_status": response.status,
            "response_content_length": response.content_length,
            "request_referrer": request.referrer,
            "request_user_agent": request.user_agent.string
        }
        #print(user_activity)
        from datastore.deps import session_scope
        with session_scope() as session:
            import crud
            object_in = {
                'user_id': request.args.get('userId'),
                'user_activity': user_activity
            }
            crud.user_activity_crud_handler.create_user_activity(db=session, obj_in=object_in)
        return response

    return app

def load_config(mode=os.environ.get('ENV')):
    """Load config."""
    if mode == 'DEV':
        from core.dev import DevelopmentConfig
        return DevelopmentConfig
    elif mode == 'LOCAL':
        from core.local import LocalConfig
        return LocalConfig
