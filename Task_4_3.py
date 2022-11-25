import re
import prettytable
from prettytable import PrettyTable


def check_parametres():
    if len(filter_attribute) == 1 and filter_attribute[0] != "":
        print("Формат ввода некорректен")
        exit()
    elif filter_attribute[0] not in ["Навыки", "Оклад", "Дата публикации вакансии", "Опыт работы", "Премиум-вакансия",
                                     "Идентификатор валюты оклада", "Название", "Название региона", "Компания", ""]:
        print("Параметр поиска некорректен")
        exit()
    elif sort_attribute not in ["Навыки", "Оклад", "Дата публикации вакансии", "Опыт работы", "Премиум-вакансия",
                                "Идентификатор валюты оклада", "Название", "Название региона", "Компания", ""]:
        print("Параметр сортировки некорректен")
        exit()
    elif need_to_reverse != "Да" and need_to_reverse != "Нет" and need_to_reverse != "":
        print("Порядок сортировки задан некорректно")
        exit()


def number_processing(number):
    number = str(int(float(number)))
    firstDigitCount = len(number) % 3
    tripletsCount = len(number) // 3
    newNumber = ""
    newNumber += number[:firstDigitCount]
    for i in range(tripletsCount):
        if newNumber != "":
            newNumber += " "
        newNumber += number[firstDigitCount + i * 3: firstDigitCount + (i + 1) * 3]
    return newNumber


def date_processing(date):
    newDate = date[8: 10] + "." + date[5: 7] + "." + date[: 4]
    return newDate


def word_processing(string):
    new_string = re.compile(r'<[^>]+>').sub('', string).replace(" ", " ").replace(" ", " ").replace("  ", " ").replace(
        "  ", " ").strip()
    if new_string in translator:
        new_string = translator[new_string]
    return new_string


def csv_reader(file_name):
    headlines_list = []
    vacancies_list = []
    length = 0
    first_element = True
    rows_count = 0
    with open(file_name, encoding="utf-8-sig") as File:
        reader = csv.reader(File)
        for row in reader:
            rows_count += 1
            if first_element:
                headlines_list = row
                length = len(row)
                first_element = False
            else:
                need_to_break = False
                if length != len(row):
                    need_to_break = True
                for word in row:
                    if word == "":
                        need_to_break = True
                if need_to_break:
                    continue
                vacancies_list.append(row)
    if rows_count == 0:
        print("Пустой файл")
        exit()
    if rows_count == 1:
        print("Нет данных")
        exit()
    return headlines_list, vacancies_list


def csv_filer(reader, list_naming):
    dictionaries_list = []
    for vacancy in reader:
        dictionary = {}
        for i in range(len(list_naming)):
            dictionary[list_naming[i]] = word_processing(vacancy[i])
        dictionaries_list.append(dictionary)
    return dictionaries_list


def formatter(row):
    new_dictionary = {}
    minSalary = ""
    maxSalary = ""
    beforeTaxes = ""
    for key in row:
        if key == "Нижняя граница вилки оклада":
            minSalary = number_processing(row[key])
        elif key == "Верхняя граница вилки оклада":
            maxSalary = number_processing(row[key]);
        elif key == "Оклад указан до вычета налогов":
            if row[key] == "Да":
                beforeTaxes = "Без вычета налогов"
            else:
                beforeTaxes = "С вычетом налогов"
        elif key == "Идентификатор валюты оклада":
            new_dictionary["Оклад"] = f"{minSalary} - {maxSalary} ({row[key]}) ({beforeTaxes})"
        elif key == "Дата публикации вакансии":
            new_dictionary[key] = date_processing(row[key])
        else:
            new_dictionary[key] = row[key]
    return new_dictionary


def cut_table(table, start_and_end, headlines, count):
    start = 0
    end = count
    start_and_end = start_and_end.split(" ")
    if start_and_end[0] == "":
        pass
    elif len(start_and_end) == 1:
        start = int(start_and_end[0]) - 1
    elif len(start_and_end) == 2:
        start = int(start_and_end[0]) - 1
        end = int(start_and_end[1]) - 1
    headlines = headlines.split(", ")
    if headlines[0] == "":
        return table.get_string(start=start, end=end)
    headlines.insert(0, "№")
    return table.get_string(start=start, end=end, ﬁelds=headlines)


def row_pass_filter(dictionary, filter_attribute):
    for key in dictionary:
        if filter_attribute[0] == "Оклад":
            if key == "Нижняя граница вилки оклада":
                if int(float(filter_attribute[1])) < int(float(dictionary[key])):
                    return False
            elif key == "Верхняя граница вилки оклада":
                if int(float(filter_attribute[1])) > int(float(dictionary[key])):
                    return False
        elif filter_attribute[0] == "Дата публикации вакансии" == key:
            if filter_attribute[1] != date_processing(dictionary[key]):
                return False
        elif filter_attribute[0] == key == "Навыки":
            for element in filter_attribute[1].split(", "):
                if element not in dictionary[key].split("\n"):
                    return False
        elif filter_attribute[0] == key:
            if filter_attribute[1] != dictionary[key]:
                return False
    return True


def sort_data_vacancies(data_vacancies, attribute, need_to_reverse):
    if need_to_reverse == "Да":
        need_to_reverse = True
    else:
        need_to_reverse = False
    if attribute == "":
        sorted_vacancies = data_vacancies
    elif attribute == "Оклад":
        sorted_vacancies = sorted(data_vacancies,
                                  key=lambda dictionary: (int(float(dictionary["Нижняя граница вилки оклада"])) +
                                                          int(float(dictionary[
                                                                        "Верхняя граница вилки оклада"]))) *
                                                         currency_to_rub[dictionary[
                                                             "Идентификатор валюты оклада"]], reverse=need_to_reverse)

    elif attribute == "Навыки":
        sorted_vacancies = sorted(data_vacancies,
                                  key=lambda dictionary: len(
                                      dictionary[attribute].split("\n")), reverse=need_to_reverse)
    elif attribute == "Опыт работы":
        expirience_dictionary = {"Нет опыта": 0, "От 1 года до 3 лет": 1, "От 3 до 6 лет": 2, "Более 6 лет": 3}
        sorted_vacancies = sorted(data_vacancies,
                                  key=lambda dictionary:
                                  expirience_dictionary[dictionary[attribute]], reverse=need_to_reverse)

    else:
        sorted_vacancies = sorted(data_vacancies, key=lambda dictionary: dictionary[attribute], reverse=need_to_reverse)
    return sorted_vacancies


def print_vacancies(data_vacancies, dic_naming):
    table = PrettyTable(hrules=prettytable.ALL, align='l')
    is_first_row = True
    number = 0
    new_data_vacancies = ({dic_naming[key]: dictionary[key] for key in dictionary} for dictionary in data_vacancies)
    print(new_data_vacancies)
    new_data_vacancies = sort_data_vacancies(new_data_vacancies, sort_attribute,
                                             need_to_reverse)
    for new_dictionary in new_data_vacancies:
        formatted_new_dictionary = formatter(new_dictionary)
        if is_first_row:
            first_row = [key for key in formatted_new_dictionary]
            first_row.insert(0, "№")
            table.field_names = first_row
            is_first_row = False
            number += 1
        if not row_pass_filter(new_dictionary, filter_attribute):
            continue
        row = [value if len(value) <= 100 else value[:100] + "..." for value in formatted_new_dictionary.values()]
        row.insert(0, number)
        table.add_row(row)
        number += 1
    if number == 1:
        print("Ничего не найдено")
        exit()

    table.max_width = 20
    table = cut_table(table, diapason, needed_columns, number - 1)
    print(table)


translator = {"name": "Название",
              "description": "Описание",
              "key_skills": "Навыки",
              "experience_id": "Опыт работы",
              "premium": "Премиум-вакансия",
              "employer_name": "Компания",
              "salary_from": "Нижняя граница вилки оклада",
              "salary_to": "Верхняя граница вилки оклада",
              "salary_gross": "Оклад указан до вычета налогов",
              "salary_currency": "Идентификатор валюты оклада",
              "area_name": "Название региона",
              "published_at": "Дата публикации вакансии",
              "noExperience": "Нет опыта",
              "between1And3": "От 1 года до 3 лет",
              "between3And6": "От 3 до 6 лет",
              "moreThan6": "Более 6 лет",
              "AZN": "Манаты",
              "BYR": "Белорусские рубли",
              "EUR": "Евро",
              "GEL": "Грузинский лари",
              "KGS": "Киргизский сом",
              "KZT": "Тенге",
              "RUR": "Рубли",
              "UAH": "Гривны",
              "USD": "Доллары",
              "UZS": "Узбекский сум",
              "True": "Да",
              "False": "Нет",
              "FALSE": "Нет",
              "TRUE": "Да"}

currency_to_rub = {"Манаты": 35.68,
                   "Белорусские рубли": 23.91,
                   "Евро": 59.90,
                   "Грузинский лари": 21.74,
                   "Киргизский сом": 0.76,
                   "Тенге": 0.13,
                   "Рубли": 1,
                   "Гривны": 1.64,
                   "Доллары": 60.66,
                   "Узбекский сум": 0.0055, }
import csv

def run_program():
    global sort_attribute, need_to_reverse, diapason, needed_columns, filter_attribute
    file_name = input("Введите название файла: ")
    filter_attribute = input("Введите параметр фильтрации: ")
    sort_attribute = input("Введите параметр сортировки: ")
    need_to_reverse = input("Обратный порядок сортировки (Да / Нет): ")
    diapason = input("Введите диапазон вывода: ")
    needed_columns = input("Введите требуемые столбцы: ")
    filter_attribute = filter_attribute.split(": ")
    check_parametres()
    headlines, vacancies = csv_reader(file_name)
    print_vacancies(csv_filer(vacancies, headlines), translator)
