import pandas as pd
import sqlite3

con = sqlite3.connect('weather.sqlite3')
weather_data = pd.read_sql_query('SELECT * FROM weather', con)