"""Логика судоку"""
import copy

def return_result(table, file):
    "Вывод результата"
    result = ""
    for i in range(9):
        for j in range(9):
            result = "".join([result, str(table[i][j])])
            if j%3 == 2:
                result = "".join([result, ' '])
        result = "".join([result, "\n"])
        if i%3 == 2:
            result = "".join([result, "\n"])
    result = "".join([result[:-1], "--------------------"])
    print(result)
    file.write(result)
    file.write("\n")

def solve_sudoku(tab, var, all_sol, diagonals, file, num_of_sol):
    "Функция-решатель"
    i, j = find_cell_to_fill(tab)
    if i == -1:
        if not all_sol:
            return_result(tab, file)
            exit(0)
        else:
            return_result(tab, file)
            return num_of_sol + 1
    for num in var[i][j]:
        copy_t = copy.deepcopy(tab)
        copy_v = copy.deepcopy(var)
        copy_t[i][j] = num
        remove_bad_numbers(copy_t, copy_v, diagonals)
        if not  is_there_solution(copy_t, copy_v):
            continue
        num_of_sol = solve_sudoku(copy_t, copy_v, all_sol, diagonals,\
                                  file, num_of_sol)
    return num_of_sol

def is_there_solution(tab, var):
    "Проверка на наличие решения"
    for i in range(9):
        for j in range(9):
            if tab[i][j] == 0 and len(var[i][j]) == 0:
                return False
    return True

def find_cell_to_fill(table):
    "Поиск пустой клетки"
    for i in range(9):
        for j in range(9):
            if table[i][j] == 0:
                return i, j
    return -1, -1

def remove_bad_numbers(tab, var, diag):
    """Удаляем из вариантов неподходящие цифры"""
    #Строки и столбцы
    for i in range(9):
        for j in range(9):
            if tab[i][j] != 0:
                for k in range(9):
                    if tab[i][j] in var[i][k]:
                        var[i][k].remove(tab[i][j])
                    if tab[i][j] in var[k][j]:
                        var[k][j].remove(tab[i][j])
    #Диагонали, если есть условие
    if diag:
        for i in range(9):
            if tab[i][i] != 0:
                for j in range(9):
                    if tab[i][i] in var[j][j]:
                        var[j][j].remove(tab[i][i])
            if tab[i][8-i] != 0:
                for j in range(9):
                    if tab[i][8-i] in var[j][8-j]:
                        var[j][8-j].remove(tab[i][8-i])
    #Квадратики 3х3
    i = 0
    j = 0
    while i < 7:
        lst_t = []
        lst_v = []
        for index_x in range(i, i + 3):
            for index_y in range(j, j + 3):
                lst_t.append(tab[index_x][index_y])
                lst_v.append(var[index_x][index_y])
        for index_x in range(9):
            if lst_t[index_x] != 0:
                for index_y in range(9):
                    if lst_t[index_x] in lst_v[index_y]:
                        lst_v[index_y].remove(lst_t[index_x])
        if j == 6:
            i += 3
            j = 0
        else:
            j += 3

def is_there_mistakes(tab, diag):
    """Проверяем корректность ввода"""
    #Строки и столбцы
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if tab[i][j] == tab[i][k]:
                    if j != k and tab[i][j] != 0:
                        print("В строке " + str(i+1) + " повторяющаяся цифра", tab[i][j])
                        return True
                if tab[j][i] == tab[k][i]:
                    if j != k and tab[j][i] != 0:
                        print("В cтолбце " + str(i+1) + " повторяющаяся цифра", tab[j][i])
                        return True
    #Квадратики 3x3
    i = 0
    j = 0
    num_of_square = 1
    while i < 7:
        lst = []
        for index_x in range(i, i + 3):
            for index_y in range(j, j + 3):
                lst.append(tab[index_x][index_y])
        for index_x in range(9):
            for index_y in range(9):
                if lst[index_x] == lst[index_y]:
                    if index_x != index_y and lst[index_x] != 0:
                        print("В квдрате 3х3 №"+str(num_of_square)+" повторяющаяся цифра", lst[index_x])
                        return True
        if j == 6:
            i += 3
            j = 0
        else:
            j += 3
        num_of_square += 1
    #Диагонали, если есть условие
    if diag:
        for i in range(9):
            for j in range(9):
                if tab[i][i] == tab[j][j]:
                    if i != j and tab[i][i] != 0:
                        print("На главной диагонали повторяющаяся цифра", tab[i][i])
                        return True
                if tab[i][8-i] == tab[j][8-j]:
                    if i != j and tab[i][8-i] != 0:
                        print("На побочной диагонали повторяющаяся цифра", tab[i][8-i])
                        return True
    return False
