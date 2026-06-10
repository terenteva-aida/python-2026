# todo. Транспонирование матрицы, transpose(matrix)
# level:hight
# Написать функцию transpose(matrix), которая выполняет транспонирование матрицы.
# Решить с использованием списковых включений.

# Пример:
# transpose([[1, 2, 3], [4, 5, 6]])

# [[1, 4], [2, 5], [3, 6]]

# ||1 2 3||      ||1 4||
# ||4 5 6||  =>  ||2 5||
#                ||3 6||

def transpose(matrix):
    """
    Транспонирует матрицу, используя списковое включение.
    
    Параметры:
    matrix (list of list): Исходная матрица размером m x n.
    
    Возвращает:
    list of list: Транспонированная матрица размером n x m.
    """
    # Проверка, что матрица не пуста
    if not matrix or not matrix[0]:
        return []
    
    # Списковое включение: для каждого столбца j создаём строку из элементов всех строк в этом столбце
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

if __name__ == "__main__":
    original = [[1, 2, 3], [4, 5, 6]]
    transposed = transpose(original)
    
    print("Исходная матрица:")
    for row in original:
        print(row)
    
    print("\nТранспонированная матрица:")
    for row in transposed:
        print(row)