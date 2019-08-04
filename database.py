## Create a database

#import path module to be able to work between platforms
from os import path
from datetime import datetime
#will be used to describe database
from sqlalchemy import(create_engine,
                       Column,
                       String,
                       Integer,
                       Float,
                       DateTime,
                       Boolean,
                       Table,
                       ForeignKey)

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


database_filename = 'weather.sqlite3'

diretory = path.abspath(path.dirname(__file__))
database_filepath = path.join(diretory, database_filename)

#create engine using file path
engine_url = 'sqlite:///{}'.format(database_filepath)

engine = create_engine(engine_url)

#the database class objects are going to inherit from
#this class
Base = declarative_base(bind=engine)

#create a configured "Session" class
Session = sessionmaker(bind=engine, autoflush=False)

#create a session
session = Session()

places_weather = Table('places_weather', Base.metadata,
                      Column('places_id', Integer, ForeignKey('places.id'), nullable = False),
                      Column('weather_id', Integer, ForeignKey('weather.place_id'), nullable=False))


class Places(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    timezone = Column(Integer)
    coordinates_lat = Column(Float)
    coordinates_lon = Column(Float)
    weather = relationship('Weather',
                             secondary = 'places_weather',
                             back_populates = 'places')

class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer)
    place_id = Column(Integer, primary_key=True)

    time = Column(DateTime, default=datetime.utcnow, primary_key=True)
    weather_description = Column(String(100), nullable=False)
    weather_main_description = Column(String(100))
    places = relationship('Places',
                             secondary = 'places_weather',
                             back_populates = 'weather')


def init_db():
    Base.metadata.create_all()


if __name__=='__main__':
    init_db()