import Task_2_1_3
import Task_4_3

choose_mode = input("Введите \"таблица\", если вам нужна таблица, введите \"pdf\", если вам нужен pdf \n")

if choose_mode == "таблица":
    Task_4_3.run_program()
elif choose_mode == "pdf":
    Task_2_1_3.run_program()
else:
    print("введены неправильные данные")
