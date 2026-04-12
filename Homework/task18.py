#todo:  Задан файл dump.txt. Необходимо для заданного файла подсчитать статистику количества
# гласных букв в тексте.

#Формат вывода:
# Количество букв a - 13
# Количество букв o - 12
# Количество букв e - 11
# .....................

with open(r'C:\Users\User\OneDrive\Рабочий стол\python\repo\Homework\dump.txt', 'r', encoding='utf-8') as file:
    text = file.read()

text = text.lower()
letters = "аеёиоуыэюяaeiouy"

# Словарь для подсчета букв и их количества
dict = {}

# Считаем гласные
for k in text:
    if k in letters:
        if k in dict:
            dict[k] += 1    #увеличиваем счетчик на 1
        else:
            dict[k] = 1     #если буква встречается впервые, присваиваем ей значение 1

# Общее количество гласных
total = sum(dict.values())  #sum - функция суммирования, .values - возвращает все значения словаря

print("Общее количество гласных букв в тексте:", total)
print("\nСтатистика по каждой гласной букве:")
#.items - возвращает коллекцию пар (кортежей), sorted - сортирует пары по первому элементу, переменные создаются автоматически на ходу
for letter, colicestvo in sorted(dict.items()):
    print(f" '{letter}' : {colicestvo} ")

if total == 0:
    print("В файле нет гласных букв.")