# todo 1: Для игры "Морской бой" файл sea_battle.py написать создание игрового поля nxn

# todo 2: В игровой матрице nxn найти кол-во всех 1

#  Задачи решить через генераторы списков (списковые включения)

import random

def create_random_field(n, num_ships):
    # Поле из нулей
    field = [[0 for i in range (n)] for i in range(n)]
    # Координаты для кораблей
    all_ships = [(i, j) for i in range(n) for j in range(n)]
    
