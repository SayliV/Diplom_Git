import os
import pandas as pd

errors = []

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
            error_status = 'Лежит не в том годе'
        elif day_index != day_folder:
            error_status = 'Лежит не в том дне'
    if len(tail) < 13:
        error_status = 'Что-то не так с именем файла'

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


file_path = r'C:\Users\SayliV\Diplom_Git\Diplom_Git\broken_files_done.txt'
process_file(file_path)