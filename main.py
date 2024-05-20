from def_file import *
#C:\Users\lenovoPC\Diplom_Git/2014.txt

# Функция нахождения в логах обработанных файлов, файлы которые побитые
file_paths = [r'C:\Users\lenovoPC\Diplom_Git\2014.txt',r'C:\Users\lenovoPC\Diplom_Git\2015d.txt',
              r'C:\Users\lenovoPC\Diplom_Git\2019.txt']
for file_path in file_paths:
    save_data_to_excel(file_path)
# file_path = r'C:\Users\lenovoPC\Downloads\Tipo_2.txt'
# save_data_to_excel(file_path)

# нахождение ошибок в записи имени файла и его располажении

# File_path = r'C:\Users\lenovoPC\Downloads\broken_files_done.txt'
# process_file (File_path)


# написать нормально меин, обработать все года и найти плохие файлы. Плохие файлы в TEQC