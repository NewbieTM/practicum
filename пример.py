from csv_processing import load_table as load_csv, save_table as save_csv
from pkl_processing import load_table as load_pkl, save_table as save_pkl
from txt_processing import save_table as save_txt
from table import Table


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