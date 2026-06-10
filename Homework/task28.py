# todo 1: Для игры "Морской бой" файл sea_battle.py написать создание игрового поля nxn

# todo 2: В игровой матрице nxn найти кол-во всех 1

#  Задачи решить через генераторы списков (списковые включения)
    
import random

def create_random_field(n, num_ships):
    # Создаём поле n x n, заполненное нулями (списковое включение)
    field = [[0 for _ in range(n)] for _ in range(n)]
    
    # Генерируем все возможные координаты (списковое включение)
    all_ships = [(i, j) for i in range(n) for j in range(n)]
    
    # Случайно выбираем num_ships уникальных координат для кораблей
    ship_positions = random.sample(all_ships, num_ships)
    
    # Расставляем корабли (единицы) на поле
    for i, j in ship_positions:
        field[i][j] = 1
    
    return field

def count_ships(field):
    # Подсчёт количества единиц через списковое включение и функцию len
    return len([cell for row in field for cell in row if cell == 1])

if __name__ == "__main__":
    n = 5          # размер поля
    num_ships = 5  # количество кораблей (единиц)
    
    # Создаём поле
    battlefield = create_random_field(n, num_ships)
    
    # Выводим поле построчно
    print("Игровое поле:")
    for row in battlefield:
        print(row)
    
    # Считаем количество единиц
    ships_count = count_ships(battlefield)
    print(f"\nКоличество кораблей (единиц): {ships_count}")