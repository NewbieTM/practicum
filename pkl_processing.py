import pickle
from table import Table

def load_table(file_path):
    try:
        with open(file_path, 'rb') as pklfile:
            table = pickle.load(pklfile)
            if not isinstance(table, Table):
                raise TypeError("Содержимое файла не является объектом Table.")
        return table
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    except pickle.UnpicklingError:
        raise ValueError("Ошибка при десериализации Pickle файла.")
    except Exception as e:
        raise e

def save_table(table, file_path):
    try:
        with open(file_path, 'wb') as pklfile:
            pickle.dump(table, pklfile)
    except Exception as e:
        raise e