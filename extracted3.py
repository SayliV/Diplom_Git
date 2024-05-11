import re
import pandas as pd
import os

file_path = r'C:\Users\lenovoPC\PycharmProjects\extracted_data_to_exel\5001-5400.txt'

def extract_data_between_paths(content):

    data_list = []
    file_name_pattern = r'([^\\]+)\s\[.*\]:'
    date_pattern = r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+'
    done_pattern = r'done\.'

    current_file_name = None
    current_date = None
    current_done = None

    for line in content.split('\n'):
        if re.search(file_name_pattern, line):
            current_file_name = re.search(file_name_pattern, line).group(1)
        elif re.search(date_pattern, line):
            current_date = re.search(date_pattern, line).group()
        elif re.search(done_pattern, line):
            current_done = 'done'

        if current_file_name and current_date and current_done:
            data_list.append({
                'File Name': current_file_name,
                'Date': current_date,
                'Done': current_done,
            })

    return current_file_name, current_date, current_done


def find_errors_and_warnings(content):
    with open(content, 'r') as file:
        text = content.read()

    error_warning_pattern = r'(ERROR|Error|WARNING|Warning):.*?done\.'

    errors_warnings_list = re.findall(error_warning_pattern, text, re.DOTALL)
    return errors_warnings_list

def save_extracted_data_to_excel(file_path):
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
                    file_name, date, processed_info = extract_data_between_paths(line)
                    warning = find_errors_and_warnings(line)
                    if any([file_name, date, processed_info, warning]):
                        data_to_excel.append({
                            'File Name': file_name,  or None # Если значение пустое, записываем None
                            'Date': date, or None
                            'Status': processed_info, or None
                            'Warning': warning or None
                        })
    except OSError as e:
        print(f"Ошибка при открытии файла: {e}")

    df = pd.DataFrame(data_to_excel)
    df.to_excel('extracted_data_from_excel.xlsx')


save_extracted_data_to_excel(file_path)
