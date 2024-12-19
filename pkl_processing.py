import pickle
from table import Table


def load_table(*file_paths):
    """
    Загрузка таблицы из одного или нескольких Pickle файлов.
    Проверяется совпадение структуры столбцов.
    """
    if not file_paths:
        raise ValueError("Не указан ни один файл для загрузки.")

    all_columns = None
    all_rows = []

    for fp in file_paths:
        try:
            with open(fp, 'rb') as pklfile:
                part_table = pickle.load(pklfile)
                if not isinstance(part_table, Table):
                    raise TypeError(f"Содержимое файла {fp} не является объектом Table.")

                if all_columns is None:
                    all_columns = part_table.columns
                else:
                    if all_columns != part_table.columns:
                        raise ValueError(f"Структура столбцов в файле {fp} не совпадает с предыдущими файлами.")

                all_rows.extend(part_table.rows)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {fp} не найден.")
        except pickle.UnpicklingError:
            raise ValueError(f"Ошибка при десериализации Pickle файла {fp}.")

    table = Table(columns=all_columns, rows=all_rows)
    return table


def save_table(table, file_path, max_rows=None):
    """
    Сохраняет таблицу в Pickle.
    Если указан max_rows, разбивает таблицу на несколько файлов.
    """
    import math
    if max_rows is not None and max_rows > 0:
        num_parts = math.ceil(len(table.rows) / max_rows)
        for i in range(num_parts):
            part_rows = table.rows[i * max_rows:(i + 1) * max_rows]
            part_filename = f"{file_path.rsplit('.', 1)[0]}_part{i + 1}.pkl"
            _save_single_pkl(table.columns, part_rows, part_filename, table.column_types)
    else:
        _save_single_pkl(table.columns, table.rows, file_path, table.column_types)


def _save_single_pkl(columns, rows, file_path, column_types):
    t = Table(columns=columns, rows=rows)
    t.column_types = column_types
    with open(file_path, 'wb') as pklfile:
        pickle.dump(t, pklfile)
