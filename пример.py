from csv_processing import load_table as load_csv, save_table as save_csv
from pkl_processing import load_table as load_pkl, save_table as save_pkl
from txt_processing import save_table as save_txt
from table import Table
from csv_processing import load_table as load_csv_multi, save_table as save_csv_multi
from pkl_processing import load_table as load_pkl_multi, save_table as save_pkl_multi
from table import concat, split, merge_tables



table = load_csv('data.csv')


table.print_table()
print(table.get_rows_by_number(0))

table.set_column_types({'ID': int,'Age': int, 'Salary': float}, by_number=False)

print(table.get_rows_by_index(1))


print(table.get_values(1)) # по колонке значения

types = table.get_column_types()
print(types)




types = table.get_column_types()
print(types)

ages = table.get_values('Age')
print(ages)


table.set_values([30, 25, 40], 'Age')

table.print_table()
save_pkl(table, 'data.pkl')

save_txt(table, 'data.txt')






print("\n=== Проверка загрузки из нескольких CSV файлов ===")
multi_table = load_csv_multi('data_part1.csv', 'data_part2.csv')
multi_table.print_table()

print("Типы столбцов после автоопределения:")
print(multi_table.get_column_types())

print("\n=== Проверка сохранения в несколько CSV файлов по max_rows ===")
save_csv_multi(multi_table, 'multi_data.csv', max_rows=1)


print("\n=== Проверка загрузки из нескольких Pickle файлов ===")
multi_table_pkl = load_pkl_multi('data_part1.pkl', 'data_part2.pkl')
multi_table_pkl.print_table()

print("Типы столбцов после автоопределения для pkl:")
print(multi_table_pkl.get_column_types())

print("\n=== Проверка сохранения в несколько Pickle файлов по max_rows ===")
save_pkl_multi(multi_table_pkl, 'multi_data.pkl', max_rows=1)


print("\n=== Проверка concat ===")
table_add = load_csv_multi('data_additional.csv')
concat_table = concat(multi_table, table_add)
concat_table.print_table()

print("\n=== Проверка split ===")
table1, table2 = split(concat_table, 3)  # Разбиваем после 3-й строки
print("Первая часть:")
table1.print_table()
print("Вторая часть:")
table2.print_table()

print("\n=== Проверка арифметических операций ===")
concat_table = concat(multi_table, table_add)
concat_table.set_column_types({'Salary': float}, by_number=False)
concat_table.add('Salary', 1000, 'Salary_plus_1000')
concat_table.print_table()

print("\n=== Проверка merge_tables по номеру строки ===")
concat_table.set_column_types({'Salary': str}, by_number=False)
another_table = load_csv_multi('data_another.csv')
merged_table_by_number = merge_tables(concat_table, another_table, by_number=True)
merged_table_by_number.print_table()

print("\n=== Проверка merge_tables по значению индекса (by_number=False) ===")
merged_table_by_index = merge_tables(concat_table, another_table, by_number=False)
merged_table_by_index.print_table()