from table import Table

def save_table(table, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as txtfile:
            txtfile.write('\t'.join(table.columns) + '\n')
            for row in table.rows:
                line = '\t'.join(str(row.get(col, '')) for col in table.columns)
                txtfile.write(line + '\n')
    except Exception as e:
        raise e

def load_table(file_path):
    raise NotImplementedError("Загрузка из текстового файла не реализована.")