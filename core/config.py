# project/config.py
import codecs
import os

from ruamel.yaml import YAML


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "ABCD"
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 2
    TOKEN_EXPIRATION_SECONDS = 1800  # 30 min

    S3_BUCKET = "profile-media-bucket"

    AWS_ACCESS_KEY = 'dummy'
    AWS_SECRET_KEY = 'dummyK'
    AWS_REGION_NAME = '=ap-northeast-1'


yaml = YAML(typ="safe", pure=True)


def get_yaml_config(config_file: str):
    # We use codecs.open because it is equivalent to Python 3 open()
    with codecs.open(config_file, "r", encoding="utf-8") as fd:
        config = yaml.load(fd.read())
    return config
