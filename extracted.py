# -*- coding: cp1251 -*-
import pandas as pd
import os
import re
file_path = r'C:\Users\lenovoPC\PycharmProjects\extracted_data_to_exel\5001-5400.txt'

# Функция извлечения имени из строки
def extract_filename_from_file(content):
    lines = content.split('\n')
    for line in lines:
        if line.startswith("C:\\Users\\"):
            file_name = line.split('\\')[-1].split()[0]
            return file_name
   # print(extract_errors_warning_from_file(content))


def extract_errors_warning_from_file(content):
    warning_error_pattern = r'(Error|ERROR|Warning|WARNING):.*'
    warning_start = content.find(warning_error_pattern)
    if warning_start != -1:
        warning_end = content.find('\n', warning_start)
        warning = content[warning_start:warning_end].strip()
        return warning

def extract_data_from_file(content):
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+'
    dates_and_times = re.findall(pattern, content)
    processed_info = 'OK' if 'done.' in content else 'NOT OK'
    dates_str = ', '.join(dates_and_times)  # Преобразуем список дат и времен в строку
    return dates_str, processed_info

# Функция записи полученных данных в Excel таблицу
def extract_data_to_excel(file_path):
    if not os.path.exists(file_path):
        print(f"Файл не найден по указанному пути: {file_path}")
        return

    data_to_excel = []
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    file_name = extract_filename_from_file(line)
                    date, processed_info = extract_data_from_file(line)
                    warning = extract_errors_warning_from_file(line)
                    if any([file_name, date, processed_info, warning]):
                        data_to_excel.append({
                            'File Name': file_name or None,  # Если значение пустое, записываем None
                            'Date': date or None,
                            'Status': processed_info or None,
                            'Warning': warning
                        })
    except OSError as e:
        print(f"Ошибка при открытии файла: {e}")

    df = pd.DataFrame(data_to_excel)
    df.to_excel('extracted_data_from_excel.xlsx')

extract_data_to_excel(file_path)
