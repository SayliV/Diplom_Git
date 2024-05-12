#функция сливаиня двух файлов в один
def merge_files(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as output:
        data1 = f1.read()
        data2 = f2.read()
        output.write(data1)
        output.write('\n\n')  # Добавляем пустую строку между содержимым файлов
        output.write(data2)
    print(f"Файлы {file1} и {file2} успешно объединены в файл {output_file}")

file1 = r'D:\Python\Extreacted_to_exel\1.txt'
file2 = r'D:\Python\Extreacted_to_exel\0.txt'
output_file = "merged_file.txt"

merge_files(file1, file2, output_file)