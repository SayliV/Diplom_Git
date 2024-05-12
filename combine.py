def merge_files():
    num_files = int(input("Введите количество файлов для объединения: "))
    file_contents = []
    for i in range(num_files):
        file_path = input(f"Введите путь к файлу {i+1}: ")
        try:
            with open(file_path, 'r') as file:
                file_contents.append(file.read())
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return
    output_file = input("Введите имя для нового объединенного файла: ")
    with open(output_file, 'w') as output:
        for content in file_contents:
            output.write(content)
            output.write('\n\n')  # Добавляем пустую строку между содержимым файлов
    print(f"{num_files} файлов успешно объединены в файл {output_file}")

merge_files()