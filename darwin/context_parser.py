from datetime import datetime
import json
import os
from dotenv import load_dotenv
from enum import Enum
import requests

class WeatherTime(Enum):
    TODAY = 1
    TOMORROW = 2

class ContextParser:
    def __init__(self, assistant_name='Darwin'):
        self.assistant_name = assistant_name
        self.file = os.path.join('..', 'additional', 'bulgarian-characteristics.json')
        self.load_json_data()
        load_dotenv()

    def load_json_data(self):
        with open(self.file, 'r', encoding='utf-8') as json_file:
            self.data = json.load(json_file)

    def getTime(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        return f'Сега е {hour} часа и {minute} минути.'

    def getDay(self):
        now = datetime.now()
        day_of_week = now.strftime('%A')
        day_of_month = now.day
        days_bulgarian_full = self.data['days']['full']
        days_mapping = {
            'Monday': days_bulgarian_full[0],
            'Tuesday': days_bulgarian_full[1],
            'Wednesday': days_bulgarian_full[2],
            'Thursday': days_bulgarian_full[3],
            'Friday': days_bulgarian_full[4],
            'Saturday': days_bulgarian_full[5],
            'Sunday': days_bulgarian_full[6]
        }
        day_of_week_bulgarian = days_mapping.get(day_of_week)
        return f'Днес е {day_of_week_bulgarian}.'

    def getDate(self):
        now = datetime.now()
        day = now.day
        month = now.month
        
        months_bulgarian_full = self.data['months']['full']
        months_mapping = {
            1: months_bulgarian_full[0],
            2: months_bulgarian_full[1],
            3: months_bulgarian_full[2],
            4: months_bulgarian_full[3],
            5: months_bulgarian_full[4],
            6: months_bulgarian_full[5],
            7: months_bulgarian_full[6],
            8: months_bulgarian_full[7],
            9: months_bulgarian_full[8],
            10: months_bulgarian_full[9],
            11: months_bulgarian_full[10],
            12: months_bulgarian_full[11]
        }
        month_bulgarian = months_mapping.get(month)

        return f'Днес е {day} {month_bulgarian}.'

    def getName(self):
        return f'Моето име е {self.assistant_name}.'

    def get_weather(self, weatherTime, lang='bg'):
        if 'WEATHER_API' not in os.environ or 'GEOLOCATION' not in os.environ:
            return 'Липсват детайли. Провери средата на изпълнение.'

        API_KEY = os.environ['WEATHER_API']
        city = os.environ['GEOLOCATION']
        
        if weatherTime == WeatherTime.TODAY:
            API_ENDPOINT = f'https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang={lang}'
        elif weatherTime == WeatherTime.TOMORROW:
            API_ENDPOINT = f'https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&lang={lang}&days=2'
        else:
            return "Невалидно време за прогнозата."

        response = requests.get(API_ENDPOINT)
        if response.status_code != 200:
            return 'Грешка при свързването с WeatherAPI.'
        
        data = response.json()

        if weatherTime == WeatherTime.TODAY:
            description = data["current"]["condition"]["text"]
            temp = data["current"]["temp_c"]
            return f"В {city} е {description} с температура {temp} градуса."

        elif weatherTime == WeatherTime.TOMORROW:
            description = data["forecast"]["forecastday"][1]["day"]["condition"]["text"]
            temp = data["forecast"]["forecastday"][1]["day"]["avgtemp_c"]
            return f"Утре в {city} ще бъде {description} с температура {temp} градуса."


    def parse(self, context):
        if context == 'time':
            return self.getTime()
        elif context == 'day':
            return self.getDay()
        elif context == 'date':
            return self.getDate()
        elif context == 'name':
            return self.getName()
        elif context == 'weather-today':
            return self.get_weather(WeatherTime.TODAY)
        elif context == 'weather-tomorrow':
            return self.get_weather(WeatherTime.TOMORROW)

