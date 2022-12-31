import cProfile
import csv


def csv_reader():
    """Создаёт список вакансий и список их параметров
    Returns:
        list: список параметров вакансий
        list: список вакансий
    """
    length = 0
    rows_count = 0
    first_element = True
    headlines_list = []
    vacancies_list = []
    for year in range(2007, 2022):
        print(str(year))
        with open(f"new_csv_files/new_csv_{year}.csv", encoding="utf-8-sig") as File:
            reader = csv.reader(File)
            for row in reader:
                if first_element:
                    rows_count += 1
                    headlines_list = row
                    length = len(row)
                    first_element = False
                else:
                    rows_count += 1
                    need_to_break = False
                    if length != len(row):
                        need_to_break = True
                    for word in row:
                        if word == "":
                            need_to_break = True
                    if need_to_break:
                        continue
                    vacancies_list.append(row)
    return headlines_list, vacancies_list


headlines_list, vacancies_list = csv_reader()
