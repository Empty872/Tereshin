import cProfile
import csv
import multiprocessing as mp
import time
from multiprocessing import Process

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
        if __name__ == '__main__':
            mp.set_start_method('spawn')
            q = mp.Queue()
            p = Process(target=foo, args=(q, length, rows_count, first_element, vacancies_list, year))
            p.start()
            length, rows_count, first_element, headlines_list = q.get()
            p.join()
    return headlines_list, vacancies_list


def working_with_file(length, rows_count, first_element, vacancies_list, year):
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
    return length, rows_count, first_element, headlines_list

global headlines_list, vacancies_list, length, rows_count, first_element

def foo(q, length, rows_count, first_element, vacancies_list, year):
    q.put(working_with_file(length, rows_count, first_element, vacancies_list, year))

pr = cProfile.Profile()
pr.enable()
headlines_list, vacancies_list = csv_reader()
pr.disable()
# pr.print_stats()
print(4)
