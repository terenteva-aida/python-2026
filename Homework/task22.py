#todo: Модифицировать программу таким образом чтобы она выводила
#  приветствие "Hello", которое до этого записано в файл text.txt
#  через метод write()


# t - работа со строками, а не байтами
f = open(r'C:/Users/User/OneDrive/Рабочий стол/Python/repo/Homework/text.txt', "w+t")
f.write("Hello\n")

# Перемещение указателя в начало файла
f.seek(0)

# Читаем содержимое файла
content = f.read

# end='' нужно, чтобы не было пустой строки, так как есть \n выше
print(content, end='')
f.close()