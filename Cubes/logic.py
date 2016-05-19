import random

HEIGHT = 0
WIDTH = 0

def get_table(height, width, c):
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height
    table = []
    for _ in range(height):
        table.append([random.randint(1, c) for _ in range(width)])
    return table

def burst(i, j, table, list_i, list_j):
    "Рекурсивно лопаем клетки"
    num = table[i][j]
    if num!= 0:
        if i < HEIGHT - 1:
            if table[i+1][j] == num:
                table[i][j] = 0
                for k in range(i+1):
                    add_to_list(list_i, k)
                add_to_list(list_j, j)
                burst(i+1, j, table, list_i, list_j)
                table[i+1][j] = 0
                add_to_list(list_i, i+1)
        if i > 0:
            if table[i-1][j] == num:
                table[i][j] = 0
                for k in range(i+1):
                    add_to_list(list_i, k)
                add_to_list(list_j, j)
                burst(i-1, j, table, list_i, list_j)
                table[i-1][j] = 0
                add_to_list(list_i, i-1)
        if j > 0:
            if table[i][j-1] == num:
                table[i][j] = 0
                for k in range(i+1):
                    add_to_list(list_i, k)
                add_to_list(list_j, j)
                burst(i, j-1, table, list_i, list_j)
                table[i][j-1] = 0
                add_to_list(list_j, j-1)
        if j < WIDTH - 1:
            if table[i][j+1] == num:
                table[i][j] = 0
                for k in range(i+1):
                    add_to_list(list_i, k)
                add_to_list(list_j, j)
                burst(i, j+1, table, list_i, list_j)
                table[i][j+1] = 0
                add_to_list(list_j, j+1)

def shift_down(table):
    "Сдвигаем вниз"
    for _ in range(HEIGHT):
        for i in range(HEIGHT - 1, 0, -1):
            for j in range(WIDTH):
                if table[i][j] == 0:
                    table[i][j] = table[i-1][j]
                    table[i-1][j] = 0

def add_to_list(list, element):
    for i in list:
        if element == i:
            return
    list.append(element)


def shift_left(table, list_j):
    "Сдвигаем влево"
    flag = True
    for _ in range(WIDTH):
        for j in range(WIDTH - 1):
            if table[HEIGHT - 1][j] == 0:
                if flag:
                    for k in range(j, len(table[0])):
                        add_to_list(list_j, k)
                for i in range(HEIGHT):
                    table[i][j] = table[i][j+1]
                    table[i][j+1] = 0

def recount_result(table):
    "Подсчёт очков"
    num = 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if table[i][j] == 0:
                num += 1
    return num

def is_there_cell_to_burst(table):
    "Проверка на наличие ходов"
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if table[i][j] != 0:
                if i != HEIGHT - 1:
                    if table[i+1][j] == table[i][j]:
                        return True
                if i != 0:
                    if table[i-1][j] == table[i][j]:
                        return True
                if j != 0:
                    if table[i][j-1] == table[i][j]:
                        return True
                if j != WIDTH - 1:
                    if table[i][j+1] == table[i][j]:
                        return True
    return False

