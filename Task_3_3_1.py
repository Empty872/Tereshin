from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from dateutil import rrule
import pandas as pd

pd.set_option("display.max_columns", None)


class CurrencyReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv(file_name)
        self.min_date = datetime.strptime(self.data['published_at'].min(), '%Y-%m-%dT%H:%M:%S%z')
        self.max_date = datetime.strptime(self.data['published_at'].max(), '%Y-%m-%dT%H:%M:%S%z')
        dictionary_currencies_all_time = self.data["salary_currency"].value_counts()
        self.date_currency_dict = {"date": []}
        for key in dictionary_currencies_all_time.keys():
            if dictionary_currencies_all_time[key] > 5000:
                self.date_currency_dict[key] = []
        self.date_currency_dict.pop("RUR")

    def read_xml(self):
        for data in rrule.rrule(rrule.MONTHLY, dtstart=self.min_date, until=self.max_date):
            tree = ET.parse(
                urlopen(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req=28/{data.strftime("%m/%Y")}d=1'))
            root = tree.getroot()
            currencies = root.findall('Valute')
            for obj in currencies:
                code = obj.find('CharCode').text
                if code in self.date_currency_dict.keys():
                    if data.strftime('%Y-%m') not in self.date_currency_dict['date']:
                        self.date_currency_dict['date'] += [data.strftime('%Y-%m')]
                    k = float(obj.find('Value').text.replace(',', '.')) / float(obj.find('Nominal').text)
                    self.date_currency_dict[code].append(k)
            if len(self.date_currency_dict['BYR']) != len(self.date_currency_dict['date']):
                self.date_currency_dict['BYR'].append(None)
        result_data = pd.DataFrame(self.date_currency_dict)
        result_data.to_csv('currencies_3.3.1.csv')


CurrencyReader("vacancies_dif_currencies.csv").read_xml()
