import csv
from table import Table

def load_table(file_path):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            columns = reader.fieldnames
            if columns is None:
                raise ValueError("CSV файл не содержит заголовков.")
            rows = [row for row in reader]
        return Table(columns=columns, rows=rows)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    except Exception as e:
        raise e

def save_table(table, file_path):
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=table.columns)
            writer.writeheader()
            for row in table.rows:
                writer.writerow(row)
    except Exception as e:
        raise e