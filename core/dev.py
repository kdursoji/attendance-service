import base64

import boto3
from environs import Env

from core.config import BaseConfig, get_yaml_config

env = Env()
env.read_env()


class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """

    PORT = 3000
    DEBUG = False
    # Logging Setup
    LOG_TYPE = env.str("LOG_TYPE", "File")  # Default is a Stream handler
    LOG_LEVEL = env.str("LOG_LEVEL", "INFO")
    LOG_DIR = env.str("LOG_DIR", "/opt/logs/nemo/")
    db_pass = 'hackathon'
    DATABASE_URL = 'postgresql+psycopg2://postgres:' + db_pass + '@evokehackathondb.cuage4x4zyme.us-east-1.rds.amazonaws.com/evokehackathondb'

    def config_logger(self, dir_path):
        import logging.config
        import os
        logging.info("Pointing to dev")
        # get log configuration
        config_file = dir_path + os.path.sep + "log_config.yaml"
        log_config = get_yaml_config(config_file=config_file)
        # set up proper logging. This one disables the previously configured loggers.
        logging.config.dictConfig(log_config)
