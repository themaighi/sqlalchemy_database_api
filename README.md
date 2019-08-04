# sqlalchemy_database_api
Create a simple database from using sqlalchemy and use it do store weather data. This is an example code on how to use sqlalchemy in order to create a small relational database.
https://www.sqlalchemy.org/

To run the code you need to do 2 steps first

## Step 1: Run the setup.py
The setup.py it will install the required packages in case you do not have them installed in your environment.
```
python setup.py build
python setup.py install
```

## Step 2: Get the API key from the OpenWeather website

https://openweathermap.org/api
You need to subscribe and get the API key. Copy the key somewhere because you will need it


# The Code

Here I will explain how to run the code and more specific part of the code

## Create a database

database.py is the first code that needs to be run. It will initialize the database, it is here that you build the architecture of your database, with all the relations.

Engine : It is used to communicate with the database (read, write, update, delete)
declarative_base : It allows you to create classes that will be mapped to tables. In this way we are able to define tables details in the class
Session: The session will establish all the conversations towards the database (you can do it directly from the engine). We will use the session to run query on the tables of the database

```
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
```

In this example I have created two class that map two specific tables, and this two tables are linked between each other with a relationship. This relationship is expressed in the table called 'places_weather'.

```
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
```

## Get data from the API

weather_api_calls.py it is an example of how you can interact with an API and how you can store the data that comes from your request in the database that you have created. In this case for this API these are the only lines of code that we need

```
    url = 'http://api.openweathermap.org/data/2.5/weather?'+input_type+'=' + input_value +\
          '&appid=' + appid

    res = requests.get(url)
    data = res.json()
```

Than there is the part that stores the results. You can see that I use the session argument in order to query the table to see if the place it already exist.
Session add = It will add in the session the new entry
Session commit = It will commit it to the database, if you do not commit it it will not add it

```
def save_weather(data):
    try:
        print('This is the city:', data['name'])
        place = session.query(Places).filter(Places.id == data['id']).one()
        print('Place already in database')
    except NoResultFound:
        print('Place not found creating')
        place = create_place(data)
        session.add(place)

    weather = create_weather(data)
    session.add(weather)
    session.commit()
```

