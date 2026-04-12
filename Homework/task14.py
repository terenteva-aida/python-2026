
#todo: Дан массив размера N. Найти минимальное растояние между одинаковыми значениями в массиве и вывести их индексы.

# Для числа 1 минимальное растояние в массиве по индексам: 0 и 7
# Для числа 2 минимальное растояние в массиве по индексам: 6 и 9
# Для числа 17 нет минимального растояния т.к элемент в массиве один.

mass = [1,2,17,54,30,89,2,1,6,2]

index_dict = {}

for i in range(len(mass)):
    val = mass[i]       #индекс
    if val not in index_dict:
        index_dict[val] = []    #создаем пустой список для нового числа
    index_dict[val].append(i)   #добавляем индекс

min_distance = float('inf')
index1 = -1     #в принципе такого индекса у нас нет
index2 = -1

for val in index_dict:
    indexes = index_dict[val]
    if len(indexes) >= 2:   #если число встречается хотя бы дважды
        for k in range(len(indexes) - 1):       # -1 нужен для того, чтобы цикл остановился на предпоследнем элементе
            a = indexes[k]
            b = indexes[k+1]
            rasstoyanie = b - a
            if rasstoyanie < min_distance:
                min_distance = rasstoyanie
                index1 = a
                index2 = b

if index1 != -1:
    print("Минимальное расстояние равно:", min_distance)
    print("Индексы:", index1, "и", index2)
    print("Значения:", mass[index1], "и", mass[index2])
else:
    print("Повторяющихся значений нет")