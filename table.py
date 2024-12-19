class Table:
    def __init__(self, columns=None, rows=None):
        self.columns = columns if columns else []
        self.rows = rows if rows else []
        self.column_types = {col: str for col in self.columns}

    def print_table(self):
        col_widths = {col: max(len(col), *(len(str(row.get(col, ''))) for row in self.rows)) for col in self.columns}


        header = ' | '.join(col.ljust(col_widths[col]) for col in self.columns)
        separator = '-+-'.join('-' * col_widths[col] for col in self.columns)
        print(header)
        print(separator)

        # Строки
        for row in self.rows:
            line = ' | '.join(str(row.get(col, '')).ljust(col_widths[col]) for col in self.columns)
            print(line)

    def get_rows_by_number(self, start, stop=None, copy_table=False):
        if stop is not None and start > stop:
            raise ValueError("Start не может быть больше Stop.")
        selected_rows = self.rows[start:stop] if stop is not None else self.rows[start:start + 1]
        if copy_table:
            import copy
            return copy.deepcopy(selected_rows)
        else:
            return selected_rows

    def get_rows_by_index(self, *vals, copy_table=False):
        selected_rows = [row for row in self.rows if row[self.columns[0]] in vals]
        if copy_table:
            import copy
            return copy.deepcopy(selected_rows)
        else:
            return selected_rows

    def get_column_types(self, by_number=True):
        types = {}
        for col in self.columns:
            types[col if not by_number else self.columns.index(col)] = self.column_types.get(col, str)
        return types

    def set_column_types(self, types_dict, by_number=True):
        for key, value in types_dict.items():
            if by_number:
                if not isinstance(key, int) or key < 0 or key >= len(self.columns):
                    raise IndexError(f"Неверный индекс столбца: {key}")
                col = self.columns[key]
            else:
                if key not in self.columns:
                    raise KeyError(f"Столбец {key} не найден.")
                col = key
            if value not in [int, float, bool, str]:
                raise ValueError(f"Неверный тип данных: {value}")
            self.column_types[col] = value
            # Приведение типов
            for row in self.rows:
                try:
                    row[col] = value(row[col])
                except ValueError:
                    raise ValueError(f"Невозможно преобразовать значение {row[col]} в {value}")

    def get_values(self, column=0):
        if isinstance(column, int):
            if column < 0 or column >= len(self.columns):
                raise IndexError(f"Столбец с индексом {column} не существует.")
            col_name = self.columns[column]
        elif isinstance(column, str):
            if column not in self.columns:
                raise KeyError(f"Столбец {column} не найден.")
            col_name = column
        else:
            raise TypeError("Параметр column должен быть int или str.")
        return [row[col_name] for row in self.rows]

    def get_value(self, column=0):
        if len(self.rows) != 1:
            raise ValueError("Таблица должна содержать ровно одну строку.")
        values = self.get_values(column)
        return values[0] if values else None

    def set_values(self, values, column=0):
        if isinstance(column, int):
            if column < 0 or column >= len(self.columns):
                raise IndexError(f"Столбец с индексом {column} не существует.")
            col_name = self.columns[column]
        elif isinstance(column, str):
            if column not in self.columns:
                raise KeyError(f"Столбец {column} не найден.")
            col_name = column
        else:
            raise TypeError("Параметр column должен быть int или str.")
        if len(values) != len(self.rows):
            raise ValueError("Количество значений не соответствует количеству строк.")
        for row, value in zip(self.rows, values):
            try:
                row[col_name] = self.column_types[col_name](value)
            except ValueError:
                raise ValueError(f"Невозможно преобразовать значение {value} в {self.column_types[col_name]}")

    def set_value(self, value, column=0):
        if len(self.rows) != 1:
            raise ValueError("Таблица должна содержать ровно одну строку.")
        if isinstance(column, int):
            if column < 0 or column >= len(self.columns):
                raise IndexError(f"Столбец с индексом {column} не существует.")
            col_name = self.columns[column]
        elif isinstance(column, str):
            if column not in self.columns:
                raise KeyError(f"Столбец {column} не найден.")
            col_name = column
        else:
            raise TypeError("Параметр column должен быть int или str.")
        try:
            self.rows[0][col_name] = self.column_types[col_name](value)
        except ValueError:
            raise ValueError(f"Невозможно преобразовать значение {value} в {self.column_types[col_name]}")
