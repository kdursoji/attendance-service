# manage.py
import os

from app import create_app, load_config

APP_ENV = ['LOCAL', 'DEV','TUNNEL']

config_name = os.getenv('FLASK_CONFIG')

if os.getenv("ENV") not in APP_ENV:
    raise Exception("Please set the ENV variable in the OS")

app = create_app(config_name)

print("Selected Environment :- " + os.getenv("ENV"))

enviroment = load_config()
dir_path = os.path.dirname(os.path.realpath(__file__))
enviroment().config_logger(dir_path)


if __name__ == '__main__':
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=3004)
