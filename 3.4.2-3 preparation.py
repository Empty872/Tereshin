import csv
from datetime import datetime
import pandas as pd

file_name = "vacancies_dif_currencies.csv"
headlines_list = []
new_files = {}
first_element = True
rows_count = 0
with open(file_name, encoding="utf-8-sig") as File:
    reader = csv.reader(File)
    for row in reader:
        if first_element:
            headlines_list = row
            first_element = False
        else:
            if row[-1][:4] in new_files.keys():
                new_files[row[-1][:4]].append(row)
            else:
                new_files[row[-1][:4]] = [headlines_list, row]
i = 0
for year in new_files:
    i += 1
    with open(f'very_new_csv_files/new_csv_{year}.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in new_files[year]:
            filewriter.writerow(row)

'''
Ссылка на файл и создание датафрейма
'''
file = 'vacancies_dif_currencies.csv'
df = pd.read_csv(file)

'''
Создаем новую колонку
'''
df['years'] = df['published_at'].apply(lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z').year)

years = df['years'].unique()

'''
Заполняем csv файлы
'''
for year in years:
    data = df[df['years'] == year]
    data.iloc[:, :6].to_csv(rf'very_new_csv_files\new_csv_{year}.csv', index=False)
