import re
import pandas as pd

 #превратить строчку в массив и по индексам путей разбить на блоки и там же по паттернам искать нужные мне данные
def extract_data_between_paths(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    data_list = []
    file_name_pattern = r'([^\\]+)\s\[.*\]:'
    date_pattern = r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+'
    done_pattern = r'done\.'
    warning_error_pattern = r'(WARNING|Error):.*'
    current_file_name = None
    current_date = None
    current_done = None
    current_warning_error = None
    for line in text.split('\n'):
        if re.search(file_name_pattern, line):
            current_file_name = re.search(file_name_pattern, line).group(1)
        elif re.search(date_pattern, line):
            current_date = re.search(date_pattern, line).group()
        elif re.search(done_pattern, line):
            current_done = 'done'
        elif re.search(warning_error_pattern, line):
            current_warning_error = re.search(warning_error_pattern, line).group()
        if current_file_name and current_date and current_done:
            data_list.append({
                'File Name': current_file_name,
                'Date': current_date,
                'Done': current_done,
                'Warning/Error': current_warning_error if current_warning_error else ''
            })
            current_file_name = None
            current_date = None
            current_done = None
            current_warning_error = None

    return data_list
def save_extracted_data_to_excel(extracted_data, filename):
    try:
        dataframe = pd.DataFrame(extracted_data)
        dataframe.to_excel(filename)
        print(f"Данные успешно сохранены в файл {filename}")
    except Exception as e:
        print(f"Произошла ошибка при сохранении данных: {e}")

# Пример использования функции
file_path =  r'D:\Python\Extreacted_to_exel\1.txt'
extracted_data = extract_data_between_paths(file_path)
save_extracted_data_to_excel(extracted_data, 'extracted_data.xlsx')