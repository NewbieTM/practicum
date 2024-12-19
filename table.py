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

    def auto_detect_types(self):

        for col in self.columns:
            values = [v for v in (row.get(col) for row in self.rows) if v is not None]

            if all(self._can_convert(v, int) for v in values):
                col_type = int

            elif all(self._can_convert(v, float) for v in values):
                col_type = float

            elif all(v.lower() in ['true', 'false'] for v in values if isinstance(v, str)):
                col_type = bool
            else:
                col_type = str

            self.column_types[col] = col_type

            for row in self.rows:
                val = row.get(col)
                if val is not None:
                    row[col] = self._convert_value(val, col_type)

    def _can_convert(self, value, to_type):
        try:
            if to_type is bool:
                return str(value).lower() in ['true', 'false']
            else:
                to_type(value)
                return True
        except:
            return False

    def _convert_value(self, value, to_type):
        if to_type is bool:
            return True if str(value).lower() == 'true' else False
        return to_type(value)

    def add(self, column1, column2, target_column='Result'):
        self._arith_operation(column1, column2, target_column, lambda x, y: x + y)

    def sub(self, column1, column2, target_column='Result'):
        self._arith_operation(column1, column2, target_column, lambda x, y: x - y)

    def mul(self, column1, column2, target_column='Result'):
        self._arith_operation(column1, column2, target_column, lambda x, y: x * y)

    def div(self, column1, column2, target_column='Result'):
        def division(x, y):
            if y == 0:
                raise ZeroDivisionError("Деление на ноль.")
            return x / y

        self._arith_operation(column1, column2, target_column, division)

    def _arith_operation(self, col1, col2, target_col, op):
        col1_name = self._get_col_name(col1)

        try:
            col2_name = self._get_col_name(col2)
            col2_is_column = True
        except (IndexError, KeyError, TypeError):
            col2_name = None
            col2_is_column = False

        t1 = self.column_types.get(col1_name, str)
        if t1 not in [int, float, bool]:
            raise TypeError(
                "Арифметические операции возможны только для столбцов типов int, float или bool (первый аргумент).")

        if col2_is_column:
            t2 = self.column_types.get(col2_name, str)
            if t2 not in [int, float, bool]:
                raise TypeError(
                    "Арифметические операции возможны только для столбцов типов int, float или bool (второй аргумент).")
        else:
            if not isinstance(col2, (int, float, bool)):
                raise TypeError("Арифметическая операция со скаляром поддерживается только для int, float или bool.")

        def to_num(val):
            if val is None:
                return 0
            if isinstance(val, bool):
                return 1 if val else 0
            return val

        results = []
        for row in self.rows:
            v1 = to_num(row.get(col1_name))
            if col2_is_column:
                v2 = to_num(row.get(col2_name))
            else:
                v2 = to_num(col2)

            if not isinstance(v1, (int, float)) or not isinstance(v2, (int, float)):
                raise ValueError("Значения не могут быть преобразованы в число.")
            res = op(v1, v2)
            results.append(res)

        if target_col not in self.columns:
            self.columns.append(target_col)
            self.column_types[target_col] = float
            for i, row in enumerate(self.rows):
                row[target_col] = results[i]
        else:
            for i, row in enumerate(self.rows):
                row[target_col] = results[i]

    def _get_col_name(self, column):
        if isinstance(column, int):
            if column < 0 or column >= len(self.columns):
                raise IndexError("Неверный индекс столбца.")
            return self.columns[column]
        elif isinstance(column, str):
            if column not in self.columns:
                raise KeyError("Столбец не найден.")
            return column
        else:
            raise TypeError("column должен быть int или str.")

    def copy(self):
        import copy
        return Table(columns=self.columns[:], rows=copy.deepcopy(self.rows), column_types=self.column_types.copy())

def concat(table1, table2):

    if table1.columns != table2.columns:
        raise ValueError("Невозможно склеить таблицы с разными наборами столбцов.")
    new_rows = table1.rows + table2.rows
    new_table = Table(columns=table1.columns, rows=new_rows)

    new_table.column_types = table1.column_types.copy()
    return new_table

def split(table, row_number):
    if row_number < 0 or row_number > len(table.rows):
        raise IndexError("Некорректный номер строки для split.")
    table1 = Table(columns=table.columns, rows=table.rows[:row_number])
    table2 = Table(columns=table.columns, rows=table.rows[row_number:])
    table1.column_types = table.column_types.copy()
    table2.column_types = table.column_types.copy()
    return table1, table2


def merge_tables(table1, table2, by_number=True):

    all_columns = list(dict.fromkeys(table1.columns + table2.columns))

    merged_types = {}
    for col in all_columns:
        t1 = table1.column_types.get(col, None)
        t2 = table2.column_types.get(col, None)
        if t1 is None:
            merged_types[col] = t2
        elif t2 is None:
            merged_types[col] = t1
        else:

            if t1 == t2:
                merged_types[col] = t1
            else:

                raise TypeError(f"Конфликт типов для столбца {col}: {t1} vs {t2}")

    rows = []

    if by_number:
        length = min(len(table1.rows), len(table2.rows))
        for i in range(length):
            r1 = table1.rows[i]
            r2 = table2.rows[i]
            merged_row = {}
            for c in all_columns:
                if c in r2 and r2[c] is not None:
                    merged_row[c] = r2[c]
                elif c in r1 and r1[c] is not None:
                    merged_row[c] = r1[c]
                else:
                    merged_row[c] = None
            rows.append(merged_row)
    else:

        first_col = table1.columns[0]

        lookup = {}
        for r in table2.rows:
            key = r.get(table2.columns[0])
            lookup[key] = r

        for r1 in table1.rows:
            key = r1.get(first_col)
            r2 = lookup.get(key, {})
            merged_row = {}
            for c in all_columns:
                v2 = r2.get(c)
                v1 = r1.get(c)
                if v2 is not None:
                    merged_row[c] = v2
                else:
                    merged_row[c] = v1
            rows.append(merged_row)

    new_table = Table(columns=all_columns, rows=rows)
    new_table.column_types = merged_types
    return new_table