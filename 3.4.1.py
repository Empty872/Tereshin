import pandas as pd
import math
from Task_3_3_1 import CurrencyReader

pd.set_option("display.max_columns", None)


class Converter:

    def __init__(self, coefficient_file, file_name, currencies):
        self.csv_currencies = pd.read_csv(coefficient_file)
        self.currencies = currencies
        self.csv_file = pd.read_csv(file_name)
        self.data = {"name": [], "salary": [], "area_name": [], "published_at": []}

    def convert(self):
        for index, row in self.csv_file.iterrows():
            if len(self.data['name']) >= 100:
                break
            salary_from, salary_to, value_curr = row["salary_from"], row["salary_to"], row["salary_currency"]
            coefficient = 1
            if math.isnan(salary_from) and math.isnan(salary_to) or value_curr not in self.currencies:
                continue
            if value_curr != 'RUR':
                coefficient = float(
                    self.csv_currencies[self.csv_currencies["date"] == row["published_at"][:7]][value_curr].values)

            if math.isnan(salary_from):
                self.data["salary"].append(salary_to * coefficient)
            elif math.isnan(salary_to):
                self.data["salary"].append(salary_from * coefficient)
            else:
                self.data["salary"].append(((salary_from + salary_to) / 2) * coefficient)

            self.data["name"].append(row["name"])
            self.data["area_name"].append(row["area_name"])
            self.data["published_at"].append(row["published_at"])

    def create_csv(self):
        result_csv_file = pd.DataFrame(self.data)
        result_csv_file.to_csv("vacancies_formatted_3_4_1.csv")


currencies = CurrencyReader("vacancies_dif_currencies.csv").date_currency_dict
currencies.pop("date")
currencies["RUR"] = []
converter = Converter("currencies_3.3.1.csv", "vacancies_dif_currencies.csv", currencies)
converter.convert()
converter.create_csv()
