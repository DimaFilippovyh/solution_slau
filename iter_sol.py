import sys
import copy



def check_diag(mat):
    """
    проверяет присутствует ли в матрице диагональное преобладание
    """
    res = True
    for i in range(len(mat)):
        agr = 0
        for j in range(len(mat[i])):
            if i != j:
                agr += abs(mat[i][j])**2
        if agr > abs(mat[i][i])**2:
            return False
    return res


def convert_mtrx(A, B):
    """
    наводит в матрице диагональное преобладание
    """
    column = 0
    while (column < len(B)):
        current_row = None
        for r in range(column, len(A)):
            if current_row is None or abs(A[r][column]) > abs(A[current_row][column]):
                current_row = r

        if current_row != column:
            A[current_row], A[column] = A[column], A[current_row]
            B[current_row], B[column] = B[column], B[current_row]

        column += 1


def simple_iter(A, B):
    """
    Метод простых итераций
    """
    n = len(B)
    eps = 0.001
    Xn = n * [0]

    res = [B[i] / A[i][i] for i in range(n)]  # свободный член / член главной дагонали

    step_iter = 0
    while step_iter <= 1000:
        step_iter += 1
        for i in range(n):
            Xn[i] = B[i] / A[i][i]
            for j in range(n):
                if i == j:
                    continue
                else:
                    Xn[i] -= A[i][j] / A[i][i] * res[j]

        flag = True
        for i in range(n):
            if abs(Xn[i] - res[i]) > eps:
                flag = False
                break

        res = Xn[:]  # заносим результат в старые значения

        if flag:
            break


    return res, step_iter


def vector_nev(A, B, X):
    """
    Вывод вектора невязки
    """
    lst_pr = []

    for i in range(len(B)):
        lst_pr.append(abs(sum([A[i][j] * X[j] for j in range(len(X))]) - B[i]))

    print("Получили вектор невязки:")
    print("\n".join("{0} =\t{1:10.5f}".format(i + 1, x) for i, x in enumerate(lst_pr)))


def main():
    A = [
        [0.42, -0.32, 0.03, 0],
        [0.11, -0.26, -0.36, 0],
        [0.12, 0.08, -0.14, -0.24],
        [0.15, -0.35, -0.18, 0]]

    B = [-0.44, -1.42, 0.83, 1.42]

    a_c = copy.deepcopy(A)
    b_c = copy.deepcopy(B)


    print("Проверяю матрицу на диагональное преобладание...")

    if check_diag(A):
        print("Проверка пройдена приступаю к решению")
    else:
        print("Матрица не прошла проверку поэтому привожу ее к диагональному преобладанию")
        convert_mtrx(A, B)
        if check_diag(A) == False:
            print("Преобразование не помогло \nрешение не наднено \nконец программы!")
            sys.exit()

    X, st = simple_iter(A, B)

    if st < 1000:
        print("Преобразование получилось решение найдено: \n")
        print(f"Всего шагов - {st}")
        
    else:
        print("Найти решение не удалось \nконец программы!")
        sys.exit()


    print("\n".join("X{0} =\t{1:10.5f}".format(i + 1, x) for i, x in enumerate(X)))
    print("\n")
    vector_nev(a_c, b_c, X)


if __name__ == "__main__":
    main()





