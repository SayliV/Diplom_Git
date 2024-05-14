import os
import openpyxl
import re

#функция нахождения ссылок и их индексов в данных
def find_data_blocks(content, **kwargs):
    lines = content.splitlines()
    path_windows = kwargs.get('Windows', 'C:\\Users')# путь для винды
    data_blocks = []
    start_index = None
    for index, line in enumerate(lines):
        if line.startswith(path_windows):
            if start_index is not None:
                data_blocks.append((start_index, index))
            start_index = index
    if start_index is not None:
        data_blocks.append((start_index, len(lines)))
    return data_blocks

#функция извлечения процесса обработки данных
def extract_data_from_content(content_short):
    content_combined = '\n'.join(content_short)
    date_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', content_combined)
    date = date_match.group().strip() if date_match else 'Дата не найдена'
    done_match = re.findall(r'\bdone\b', content_combined)
    processed_info = 'OK' if done_match else 'NOT OK'
    return date, processed_info

#функция нахождеиня ошибок и предупреждеинй в данных
def extract_errors_warning_from_content(content_short):
    content_combined = '\n'.join(content_short)
    # Паттерн для поиска ошибок (ERROR) и предупреждений (WARNING)
    pattern_error = r'(?:\[ERROR\]|ERROR).*?\n'
    pattern_warning = r'(?:\[WARNING\]|WARNING).*?\n'
    # Поиск ошибок
    match_error = re.search(pattern_error, content_combined, re.DOTALL)
    if match_error:
        error = match_error.group().strip()
        return error
    # Поиск предупреждений
    match_warning = re.search(pattern_warning, content_combined, re.DOTALL)
    if match_warning:
        warning = match_warning.group().strip()
        return warning
    return "NO ERROR or WARNING"

#функция нахождения имени в данных
def extract_filenames_from_content(content_short):
    filenames = []
    for line in content_short:
        if line.startswith("C:\\Users\\"):
            file_name = line.split('\\')[-1].split()[0]
            filenames.append(file_name)
    return filenames

#функция записи полученных данных в EXCEl файл
def extract_data_from_file(file_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Name', 'Date', 'Processed Info', 'Error or Warning'])
    with open(file_path, 'r') as file:
        content = file.read()
        #print(content)
        data_blocks = find_data_blocks(content)
        #print(data_blocks)
        for start_index, end_index in data_blocks:
            content_short = content.splitlines()[start_index:end_index]
            #print(content_short)
            names = extract_filenames_from_content(content_short)
            for name in names:
                date, processed_info = extract_data_from_content(content_short)
                error = extract_errors_warning_from_content(content_short)
                ws.append([name, date, processed_info, error])
        wb.save('output.xlsx')
    print('Файл output.xlsx сохранён в:', os.getcwd())
