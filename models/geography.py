from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean, String, Text
from sqlalchemy.orm import relationship

from datastore.base_class import Base


class Countries(Base):
    __tablename__ = 'countries_t'
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


class States(Base):
    __tablename__ = 'states_t'
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(250), nullable=False)
    country_id = Column("country_id", Integer, ForeignKey('countries_t.id'), nullable=False)

    country = relationship('Countries', backref='States', lazy=True)

    def serialize(self):
        data = {
            'id': self.id,
            'name': self.name,
            'country_id': self.country_id
        }
        return data


class Cities(Base):
    __tablename__ = 'cities_t'
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(250), nullable=False)
    state_id = Column("state_id", Integer, ForeignKey('states_t.id'), nullable=False)

    state = relationship('States', backref='Cities', lazy=True)

    def serialize(self):
        data = {
            'id': self.id,
            'name': self.name,
            'state_id': self.state_id
        }
        return data
