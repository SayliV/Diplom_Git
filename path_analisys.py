import os
import pandas as pd

def compare_year_folder_and_extension(file_path):
    # Получаем путь к папке файла без последнего компонента (имя файла)
    folder_path = os.path.dirname(file_path)
    head, tail = os.path.split(file_path)
    # Получаем имя папки 2019 года
    year_folder = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(folder_path))))
    day_folder = os.path.basename(os.path.dirname(os.path.dirname(folder_path)))
    # Получаем все расширения файла
    file_name = os.path.basename(file_path)
    file_extensions = file_name.split('.')[1:]
    # Ищем последнее расширение, начиная с конца списка
    last_extension = file_extensions[0]
    # Проверяем, совпадают ли имя папки и последнее расширение файла
    index_expansion = last_extension[0:2]
    day_index = tail[4:7]
    last_index_year = year_folder[2:4]
    error_status = ''
    # сравнение переменных года папки и года дня, аналогично с днём
    if index_expansion == last_index_year and day_index == day_folder:
        error_status = 'OK'
    # если не выполняется условие, то отдельно находится причина
    else:
        if index_expansion != last_index_year:
            error_status = 'Wrong year'
        elif day_index != day_folder:
            error_status = 'Wrong day'
    if len(tail) < 13:
        error_status = 'Wrong file name'
    # вывод полученных данных
    return error_status, day_index, last_index_year

# основная функция отвечающия за запуск подфункции
def process_file(file_path):
    # создание массива для дальнейшей его записи в excel формат
    data = []
    # создание excel файла с записью в него полученных данных
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
    # название полученного excel файла
    df.to_excel('all_files_table.xlsx', index=False)

# укажите путь где лежит файл с путями на сервере, где находятся файлы
file_path = r'C:\Users\SayliV\Diplom_Git\Diplom_Git\broken_files_done.txt'
process_file(file_path)