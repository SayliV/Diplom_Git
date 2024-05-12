import openpyxl
import re

#функция нахождения ссылок и их индексов в данных
def find_data_blocks(content):
    lines = content.splitlines()
    data_blocks = []
    start_index = None
    for index, line in enumerate(lines):
        if line.startswith('C:\\Users\\lenovoPC\\Desktop\\files GNSS\\obs\\'):
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
    pattern = r'\[WARNING\].*?\n'
    match = re.search(pattern, content_combined, re.DOTALL)
    if match:
        warning = match.group().strip()
        return warning
    else:
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
        data_blocks = find_data_blocks(content)
        for start_index, end_index in data_blocks:
            content_short = content.splitlines()[start_index:end_index]
            names = extract_filenames_from_content(content_short)
            for name in names:
                date, processed_info = extract_data_from_content(content_short)
                error = extract_errors_warning_from_content('\n'.join(content_short))
                ws.append([name, date, processed_info, error])
        wb.save('output.xlsx')

# Вставте в file_path ссылку на txt файл с обработанными данными
file_path = r'D:\Python\Extreacted_to_exel\1.txt'
extract_data_from_file(file_path)