import enum
from enum import Enum
import datetime
from traceback import print_exc

import jwt
from flask import current_app
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean, String, Text, func, JSON
from sqlalchemy.orm import relationship

from app import bcrypt
from datastore.base_class import Base
from models.geography import Cities, States
from models.profile_imge import ProfileImages


class User(Base):
    __tablename__ = 'users_t'

    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String(250), nullable=False)
    last_name = Column("last_name", String(250), nullable=False)
    middle_name = Column("middle_name", String(250))
    mobile_number = Column("mobile_number", Integer, nullable=False)
    email = Column("email", String(100), nullable=False)
    dob_dtm = Column('dob', DateTime(timezone=True), nullable=False)
    introduction = Column("intro", Text, nullable=False)
    address = Column("address", Text, nullable=False)
    city_id = Column("city_id", Integer, ForeignKey('cities_t.id'))
    pincode = Column("pincode", Integer, nullable=False)
    gender = Column("gender", String(1), nullable=False)
    user_name = Column("user_name", String(100), nullable=False)
    password = Column("password", String(100), nullable=False)
    profile_pic_location = Column("profile_pic_location", String(300))
    is_blocked = Column("is_blocked", Boolean, default=False)
    blocked_on = Column("blocked_on", DateTime(timezone=True))
    registered_on = Column("registered_on", DateTime(timezone=True), default=func.now())
    last_login_on = Column("last_login", DateTime(timezone=True))

    city = relationship('Cities', backref='Users', lazy=True)

    def serialize(self):
        profile = None
        city = None

        if self.city:
            city = {'id': self.city.id, 'name': self.city.name},

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'mobile_number': self.mobile_number,
            'email': self.email,
            'dob_dtm': self.dob_dtm,
            'introduction': self.introduction,
            'address': self.address,
            'city': city,
            'pincode': self.pincode,
            'gender': self.gender,
            'user_name ': self.user_name,
            'profile_pic_location': self.profile_pic_location,
            'registered_on': self.registered_on,
            'last_login_on': self.last_login_on
        }

    def encode_auth_token(self, user_id):
        """Generates the auth token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            print_exc()
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token - :param auth_token: - :return: integer|string"""
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class UserActivity(Base):
    __tablename__ = 'user_activity_t'

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey('users_t.id'), nullable=False)
    user_activity = Column("activity_object", JSON, nullable=False)
    user_activity_on = Column("user_activity_on", DateTime(timezone=True), default=func.now())
