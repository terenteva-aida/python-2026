# for цель in объект
# операторы if проверка: break (выход из цикла)
# if проверка: continue (переход в начало цикла)
# else: ветка выполняется, если не было выхода с помощью break

input_list = [10, "S", 15, "А", 1]
for item in input_list:
    print(item)

print(list(range(5))) # считает число элементов для количества итераций цикла

counter = 0
for i in list(range(5)):
    counter +=1
print(counter)

for x in range(3):
    print('result', x)

for i in "Hello world":
    # print(i)
    if i == "o":
        break
    print(i)

for i in "Hello world":
    if i == "o":
        continue
    print(i)

# pass - пропуск кода, заглушка (если на данный момент не используем)

# while True: тут проверяется условие
#     print("!") тут выполняется действие

# while - когда не знаем количество элементов, for - знаем