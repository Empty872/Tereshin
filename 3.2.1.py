import csv

file_name = input("Введите нащвание файла: ")
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
    with open(f'new_csv_files/new_csv_{year}.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in new_files[year]:
            filewriter.writerow(row)
