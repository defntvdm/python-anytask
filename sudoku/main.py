#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Николаев Вадим КБ-201 2015
"""

import argparse
import logic

def get_args():
    """Парсим аргументы"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="input.txt", \
                        help="Файл с входными данными (по умолчанию input.txt)")
    parser.add_argument("-o", "--output", default="output.txt", \
                        help="Файл на выходе (по умолчанию output.txt)")
    parser.add_argument("-a", "--all", action="store_true", \
                        help="Вывести все решения")
    parser.add_argument("-d", "--diagonals", action="store_true", \
                        help="Дополнительное условие на диагонали")
    return parser.parse_args()


def get_table(inp):
    """Считываем данные"""
    num = 0
    table = []
    try:
        with open(inp) as file:
            for line in file:
                if line == "\n":
                    continue
                num += 1
                lst = []
                for symbol in line:
                    if symbol <= '9' and symbol >= '0':
                        lst.append(int(symbol))
                if len(lst) < 9:
                    print("Недостаточно цифр в строке", num)
                    exit(0)
                elif len(lst) > 9:
                    print("Слишком много цифр в строке", num)
                    exit(0)
                else:
                    table.append(lst)
        if len(table) < 9:
            print("Недостаточно строк")
            exit()
        elif len(table) > 9:
            ans = input("Слишком много строк, продолжить с первыми 9? [Д/н]   ")
            ans = ans.lower()
            if ans == "y" or ans == "yes" or ans == "д" or ans == "да":
                return table[:9]
            exit(0)
        else:
            return table
    except FileNotFoundError:
        print("Нет файла", inp)
        exit(0)

def get_variants(tab):
    """Таблица вариантов постановки цифры"""
    variants = []
    for i in range(9):
        line = []
        for j in range(9):
            if tab[i][j] == 0:
                line.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                line.append([])
        variants.append(line)
    return variants

def main():
    "Старт"
    num = 0
    args = get_args()
    table = get_table(args.input)
    if logic.is_there_mistakes(table, args.diagonals):
        exit(0)
    variants = get_variants(table)
    logic.remove_bad_numbers(table, variants, args.diagonals)
    if not logic.is_there_solution(table, variants):
        print("Нет решений")
        exit(0)
    with open(args.output, 'w') as out_file:
        num = logic.solve_sudoku(table, variants, args.all, args.diagonals, out_file, num)

if __name__ == "__main__":
    main()


__author__ = 'vadim'
