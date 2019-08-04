import pandas as pd
import requests
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from database import Places, Weather, session


def create_place(data):
    place = Places(id=data['id'],
                   name=data['name'],
                   timezone=data['timezone'],
                   coordinates_lat=data['coord']['lat'],
                   coordinates_lon=data['coord']['lon'])

    return place


def create_weather(data):
    weather = Weather(id=data['weather'][0]['id'],
                      place_id=data['id'],
                      time=datetime.now(),
                      weather_description=data['weather'][0]['description'],
                      weather_main_description=data['weather'][0]['main'])

    return weather


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


def run(appid):

    input_type = input(
            'Define if you want to search using the city name (write q), '
            'the city id (write id), the city zip code (write zip): ')

    while input_type not in ['zip', 'id', 'q']:
        print('The input type is wrong')
        input_type = input(
            'Define if you want to search using the city name (write q), '
            'the city id (write id), the city zip code (write zip): ')

    input_value = input('Of which city/id/zip code would you like to know the weather :')

    url = 'http://api.openweathermap.org/data/2.5/weather?'+input_type+'=' + input_value +\
          '&appid=' + appid

    res = requests.get(url)
    data = res.json()
    save_weather(data)


if __name__ == '__main__':
    #dbb56787bf749145c1e67e03e9470194
    input_continue = 'yes'
    input_appid = input('Please give me you api Key')
    while input_continue != 'no':
        run(appid=input_appid)
        input_continue = input('Do you want to pull other weather data? If you type no it will stop')
