import pandas as pd
import sqlite3


class DBConverter:
    """Класс для конвертации csv в db.
    Attributes:
        full_csv_path(str): путь до файла csv.
        db_path(str): путь до директории с базой данных.
        db_name(str): название базы данных.
    """

    def __init__(self, full_csv_path: str, db_name: str):
        """Инициализация. создание базы данных из csv-файла.
        Args:
            full_csv_path(str): путь до файла csv.
            db_name(str): название базы данных.
        """
        self.full_csv_path = full_csv_path
        self.db_name = db_name
        self.convert_csv()

    def convert_csv(self):
        """Конверация csv с валютами в db с валютами."""
        con = sqlite3.connect(self.db_name)
        con.execute("DROP TABLE IF EXISTS currencies")
        pd.read_csv(self.full_csv_path).to_sql("currencies", con, index=False)
        for element in con.execute("SELECT * FROM currencies").fetchall():
            print(element)


converter = DBConverter("currencies_3.3.1.csv", "currencies.db")
