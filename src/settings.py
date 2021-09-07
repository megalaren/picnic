import os

from dotenv import load_dotenv

load_dotenv()


DB_HOST = os.getenv('DATABASE_HOST')
DB_PORT = os.getenv('DATABASE_PORT')
DB_NAME = os.getenv('DATABASE_NAME')
DB_USER = os.getenv('DATABASE_USER')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD')

# SQLALCHEMY_DATABASE_URL = 'sqlite:///test.db'
SQLALCHEMY_DATABASE_URL = (f'postgresql://{DB_USER}:{DB_PASSWORD}'
                           f'@{DB_HOST}:{DB_PORT}/{DB_NAME}')

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_URL = ('https://api.openweathermap.org/data/2.5/weather'
               '?units=metric&q={city}'
               f'&appid={WEATHER_API_KEY}')
