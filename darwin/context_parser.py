from datetime import datetime
import json
import os

class ContextParser:
    def __init__(self, assistant_name='Darwin'):
        self.assistant_name = assistant_name
        self.file = os.path.join('..', 'additional', 'bulgarian-characteristics.json')
        self.load_json_data()

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
    
    def parse(self, context):
        if context == 'time':
            return self.getTime()
        elif context == 'day':
            return self.getDay()
        elif context == 'date':
            return self.getDate()
        elif context == 'name':
            return self.getName()
