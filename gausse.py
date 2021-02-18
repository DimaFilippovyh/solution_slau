import sys
import copy
import numpy as np

A = [[0.42, -0.32, 0.03, 0],
     [0.11, -0.26, -0.36, 0],
     [0.12, 0.08, -0.14, -0.24],
     [0.15, -0.35, -0.18, 0]]

B = [-0.44, -1.42, 0.83, 1.42]

# A = [[1, 1],
#     [2, 2]]

# B = [1, 2]

# A = [[1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]]

# B = [2, 5, 7]

# A = [[3, -5, 2, 4],
#     [7, -4, 1, 3],
#     [5, 7, -4, -6]]

# B =  [2, 5, 3]

print_f = open("step_res_gauss.txt", "w")


def beaut_print(A, B, selected):
    """
    Вывод системы на экран
    """
    for row in range(len(B)):
        print_f.write("(")
        for col in range(len(A[row])):
            print_f.write(
                "\t{1:5.2f}{0}".format(" " if (selected is None or selected != (row, col)) else "*",\
                 A[row][col]))
        print_f.write("\t) * (\tX{0}) = (\t{1:10.2f})".format(row + 1, B[row]))
        print_f.write("\n")


def swap_rows(A, B, row1, row2):
    """
    Меняет местами 2 строки
    """
    A[row1], A[row2] = A[row2], A[row1]
    B[row1], B[row2] = B[row2], B[row1]


def divide_row(A, B, row, divider):
    """
    деление строки системы на число
    """
    A[row] = [a / divider for a in A[row]]
    B[row] /= divider


def combine_rows(A, B, row, source_row, weight):
    """
    сложение 2 строк или умножение на число
    """
    A[row] = [(a + k * weight) for a, k in zip(A[row], A[source_row])]
    B[row] += B[source_row] * weight


def check_silution(A, B, selected):
    """
    Проверяем сколько рещений имеется у матрицы: одно/много/нет ни одного
    """
    c_r, r = selected
    if abs(A[c_r][r]) < 0.0001:
        if abs(B[r]) < 0.0001:
            print("Решений бесконечное множество")
        else:
            print("решений нет")

        sys.exit()


def check_silution_with_rank(a, b):
    a_np = np.array(a)
    b_np = np.array(width_matr(a, b))

    rank_a = np.linalg.matrix_rank(a_np)
    rank_b = np.linalg.matrix_rank(b_np)

    if rank_a == rank_b == len(a[0]):
        return None
    elif rank_a == rank_b and rank_a != len(a[0]):
        print("Решений бесконечное множество")
        sys.exit()
    else:
        print("решений нет")
        sys.exit()


def gauss(A, B):
    """
    Метод Гаусса, приведение к треугольному виду
    """
    column = 0
    while column < len(B):

        print_f.write("Ищем максимальный по модулю элемент в {0}-м столбце: \n".format(column + 1))
        current_row = None
        for r in range(column, len(A)):
            if current_row is None or abs(A[r][column]) > abs(A[current_row][column]):
                current_row = r

        # check_silution(A, B, (current_row, column))  если не с помощью ранга то активировать

        beaut_print(A, B, (current_row, column))

        if current_row != column:
            print_f.write("Переставляем строку с найденным элементом повыше: \n")
            swap_rows(A, B, current_row, column)
            beaut_print(A, B, (column, column))

        print_f.write("Нормализуем строку с найденным элементом:\n")
        divide_row(A, B, column, A[column][column])
        beaut_print(A, B, (column, column))

        print_f.write("Обрабатываем нижележащие строки: \n")
        for r in range(column + 1, len(A)):
            combine_rows(A, B, r, column, -A[r][column])
        beaut_print(A, B, (column, column))

        column += 1

    print_f.write("Матрица приведена к треугольному виду, считаем решение... \n")
    X = [0 for b in B]
    for i in range(len(B) - 1, -1, -1):
        X[i] = B[i] - sum(x * a for x, a in zip(X[(i + 1):], A[i][(i + 1):]))

    print("Получили ответ:")
    print("\n".join("X{0} =\t{1:10.5f}".format(i + 1, x) for i, x in enumerate(X)))

    return X


def vector_nev(A, B, X):
    """
    Вывод вектора невязки
    """
    lst_pr = []

    for i in range(len(B)):
        lst_pr.append(abs(sum([A[i][j] * X[j] for j in range(len(X))]) - B[i]))

    print("Получили вектор невязки:")
    print("\n".join("{0} =\t{1:10.5f}".format(i + 1, x) for i, x in enumerate(lst_pr)))


def width_matr(a, b):
    """
    Создает расширенную матрицу
    """
    return [a[i] + [b[i]] for i in range(len(b))]



def main():
    print_f.write("Исходная система: \n")
    beaut_print(A, B, None)

    a_c = copy.deepcopy(A)
    b_c = copy.deepcopy(B)
    check_silution_with_rank(a_c, b_c)
    
    a_c = copy.deepcopy(A)
    b_c = copy.deepcopy(B)

    print_f.write("Решаем: \n")
    x = gauss(A, B)

    vector_nev(a_c, b_c, x)


if __name__ == "__main__":
    main()




