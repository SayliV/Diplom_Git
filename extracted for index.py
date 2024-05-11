import openpyxl
import os
#функция нахождения ссылок и их индексов
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

def extract_data_from_content(content_short):
    date_start = content_short.find('processing...') + len('processing...')
    date_end = content_short.find('done.', date_start)
    date = content_short[date_start:date_end].strip()
    processed_info = 'Обработка завершена' if 'done.' in content_short else 'Обработка не завершена'
    return date, processed_info


def extract_errors_warning_from_content(content):
    warning_start = content.find('[WARNING]')
    if warning_start != -1:
        warning_end = content.find('\n', warning_start)
        warning = content[warning_start:warning_end].strip()
        return warning
    else:
        return "No warning found in the file"


def extract_filenames_from_content(content_short):
    filenames = []
    for line in content_short:
        if line.startswith("C:\\Users\\"):
            file_name = line.split('\\')[-1].split()[0]
            filenames.append(file_name)
    return filenames


def extract_data_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        data_blocks = find_data_blocks(content)
        wb = openpyxl.load_workbook('output.xlsx') if os.path.exists('output.xlsx') else openpyxl.Workbook()
        sheet = wb.active
        row_number = sheet.max_row + 1
        for start_index, end_index in data_blocks:
            content_short = content.splitlines()[start_index:end_index]
            names = extract_filenames_from_content(content_short)
            for name in names:
                date, processed_info = extract_data_from_content(content)
                #print(date, processed_info)
                error = extract_errors_warning_from_content(content[start_index:end_index])
                sheet[f'A{row_number}'] = name
                sheet[f'B{row_number}'] = date
                sheet[f'C{row_number}'] = processed_info
                sheet[f'D{row_number}'] = error
                row_number += 1
        wb.save('output.xlsx')


# Пример использования функции
file_path = r'D:\Python\Extreacted_to_exel\1.txt'
extract_data_from_file(file_path)