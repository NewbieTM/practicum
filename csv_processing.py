import csv
from table import Table


def load_table(*file_paths):

    if not file_paths:
        raise ValueError("Не указан ни один файл для загрузки.")

    all_columns = None
    all_rows = []

    for fp in file_paths:
        try:
            with open(fp, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if reader.fieldnames is None:
                    raise ValueError(f"CSV файл {fp} не содержит заголовков.")

                if all_columns is None:
                    all_columns = reader.fieldnames
                else:
                    if all_columns != reader.fieldnames:
                        raise ValueError(f"Структура столбцов файла {fp} не совпадает с предыдущими файлами.")

                for row in reader:
                    all_rows.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {fp} не найден.")

    table = Table(columns=all_columns, rows=all_rows)
    return table


def save_table(table, file_path, max_rows=None):
    """
    Сохраняет таблицу в CSV файл. Если max_rows задан,
    разбивает таблицу на несколько файлов.
    """
    import math
    if max_rows is not None and max_rows > 0:
        # Разбиваем по max_rows
        num_parts = math.ceil(len(table.rows) / max_rows)
        for i in range(num_parts):
            part_rows = table.rows[i * max_rows:(i + 1) * max_rows]
            part_filename = f"{file_path.rsplit('.', 1)[0]}_part{i + 1}.csv"
            _save_single_csv(table.columns, part_rows, part_filename)
    else:
        _save_single_csv(table.columns, table.rows, file_path)


def _save_single_csv(columns, rows, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
