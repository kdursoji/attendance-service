from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean, String, Text
from sqlalchemy.orm import relationship

from datastore.base_class import Base


class organizations(Base):
    __tablename__ = 'organizations_t'

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(250), nullable=False)
    address = Column("address", Text, nullable=False)
    city_id = Column("city_id", Integer, ForeignKey('cities_t.id'))
    duration_from = Column("duration_from", DateTime(timezone=True))
    duration_to = Column("duration_to",DateTime(timezone=True))
    is_current_organization = Column("is_current_organization", Boolean, default=False)
    user_id = Column("user_id", Integer, ForeignKey('users_t.id'))
    position_id = Column("position_id", Integer, ForeignKey('positions_t.id'))
    team_id = Column("team_id", Integer, ForeignKey('teams_t.id'))

    city = relationship('Cities', backref='organizations', lazy=True)
    user = relationship('User', backref='organizations', lazy=True)
    position = relationship('Positions', backref='organizations', lazy=True)
    teams = relationship('Teams', backref='organizations', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city_id': self.city_id,
            'duration_from': self.duration_from,
            'duration_to': self.duration_to,
            'is_current_organization ': self.is_current_organization,
            'poistion': {
                'id': self.position.id,
                'name': self.position.name
            },
            'team': {
                'id': self.teams.id,
                'name': self.teams.name
            }
        }


class Positions(Base):
    __tablename__ = 'positions_t'
    id = Column("id", Integer, primary_key=True)
    shortname = Column("shortname", String(250), nullable=False)
    name = Column("name", String(250), nullable=False)

    def serialize(self):
        data = {
            'id': self.id,
            'shortName': self.shortname,
            'name': self.name
        }
        return data


class Teams(Base):
    __tablename__ = 'teams_t'
    id = Column("id", Integer, primary_key=True)
    shortname = Column("shortname", String(250), nullable=False)
    name = Column("name", String(250), nullable=False)

    def serialize(self):
        data = {
            'id': self.id,
            'shortName': self.shortname,
            'name': self.name
        }
        return data
