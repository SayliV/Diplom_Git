import os
import openpyxl
import re
import pandas as pd

################################################# функции отвечающие за ваполнение обработки данных и записи в эксель
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
    date_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d{6})?', content_combined)
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
def save_data_to_excel(file_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Name', 'Date', 'Processed Info', 'Error or Warning'])
    with open(file_path, 'r') as file:
        content = file.read()
        data_blocks = find_data_blocks(content)
        for start_index, end_index in data_blocks:
            content_short = content.splitlines()[start_index:end_index]
            names = extract_filenames_from_content(content_short)
            for name in names:
                date, processed_info = extract_data_from_content(content_short)
                error = extract_errors_warning_from_content(content_short)
                ws.append([name, date, processed_info, error])
        output_file_name = os.path.basename(file_path).split('.')[0] + '.xlsx'
        wb.save(output_file_name)
    print(f'File', output_file_name, 'saved in:', os.getcwd())

############################################################### участок с функциями отвечающими за анализ RINEX файла
def compare_year_folder_and_extension(file_path):

    # Получаем путь к папке файла без последнего компонента (имя файла)
    folder_path = os.path.dirname(file_path)
    head, tail = os.path.split(file_path)

    # Получаем имя папки 2019 года
    year_folder = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(folder_path))))
    day_folder = os.path.basename(os.path.dirname(os.path.dirname(folder_path)))
    # print(day_folder)
    # print("Tail:", tail)

    # Получаем все расширения файла
    file_name = os.path.basename(file_path)
    file_extensions = file_name.split('.')[1:]
    # print(file_extensions)

    # Ищем последнее расширение, начиная с конца списка
    last_extension = file_extensions[0]
    # print(last_extension)

    # Проверяем, совпадают ли имя папки и последнее расширение файла
    index_expansion = last_extension[0:2]
    # print(index_expansion)
    day_index = tail[4:7]
    # print(day_index)
    last_index_year = year_folder[2:4]
    # print(last_index_year)
    error_status = ''

    if index_expansion == last_index_year and day_index == day_folder:
        error_status = 'OK'
    else:
        if index_expansion != last_index_year:
            error_status = 'Wrong year'
        elif day_index != day_folder:
            error_status = 'Wrong day'
    if len(tail) < 13:
        error_status = 'Wrong name'

    return error_status, day_index, last_index_year

def process_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            result = compare_year_folder_and_extension(line.strip())
            data.append({
                'File Name': os.path.basename(line.strip()),
                'Year': result[2] if result else '',
                'Day': result[1] if result else '',
                'Error Status': result[0] if result else ''
            })

    df = pd.DataFrame(data)
    df.to_excel('all_files_table.xlsx', index=False)