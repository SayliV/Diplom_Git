import re

def find_data_block(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    start_index = None
    end_index = None
    for index, line in enumerate(lines):
        if line.startswith('C:\\Users\\lenovoPC\\Desktop\\files GNSS\\obs\\'):
            start_index = index
            break
    if start_index is not None:
        for index in range(start_index + 1, len(lines)):
            if not lines[index].startswith('C:\\Users\\lenovoPC\\Desktop\\files GNSS\\obs\\'):
                end_index = index
                break
    if start_index is not None and end_index is not None:
        return start_index, end_index
    else:
        print("Не удалось найти блок данных")
        return None, None
# функция извлечения имени из пути
def extract_filename_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        lines = content.split('\n')
        for line in lines:
            if line.startswith("C:\\Users\\"):
                file_name = line.split('\\')[-1].split()[0]
                return file_name
# функция извлечения даты из процесса обработки
def extract_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        date_start = data.find('processing...') + len('processing...')
        date_end = data.find('done.', date_start)
        date = data[date_start:date_end].strip()
        processed_info = 'Обработка завершена' if 'done.' in data else 'Обработка не завершена'
        return date, processed_info
# функция извлечения ошибок и предупреждений из процесса обработки
def extract_errors_warning_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        warning_start = content.find('[WARNING]')
        if warning_start != -1:
            warning_end = content.find('\n', warning_start)
            warning = content[warning_start:warning_end].strip()
            return warning
        else:
            return "No warning found in the file"
def extract_data(file_path, start_index, end_index, date):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data_found =[]
    for line_number, line in enumerate(lines[start_index:end_index + 1], start=start_index):
        file_match = re.search(r'(\w+\.14d)', line)
        last_word_match = re.search(r'done\.', line)  # Уточним шаблон для "done."
        print(f"Имя файла: {file_match.group(0)}\nДата: {date}\nПоследнее слово: {last_word_match.group(0)}")
        print(line)  # Выводим строку, которая соответствует всем шаблонам

    if not data_found:
        print("Данные не найдены")


# Пример использования функции
file_path = r'D:\Python\Extreacted_to_exel\1.txt'
start_index, end_index = find_data_block(file_path)
date= extract_data_from_file(file_path)
extract_data(file_path, start_index, end_index, date)
