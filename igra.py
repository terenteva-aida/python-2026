# Угадай число, надо загадть число от 1 до 100. Пользователь вводит число, пока не угадает, 5 попыток.

import random
rn = random.randint(1, 100)
counter = 5

for i in range(counter, 0, -1):
    print(f"Осталось попыток: {i}")
    inp = input("Введите число: ")
        
    num = int(inp)
    
    if num == rn:
        print(f"Поздравляю! Вы угадали число {rn}")
        break
    elif num < rn:
        print("Загаданное число больше")
    else:
        print("Загаданное число меньше")
else:
    print(f"Вы проиграли. Загаданное число было {rn}")