import numpy as np
import copy


def read_file(file_name):
    with open(file_name) as f:
        content = f.readlines()
    matrix = np.zeros((9,9))
    row_count = 0
    for line in content:
        elems = line.split(" ")
        column_count = 0
        for elem in elems:
            elem = elem.replace("\n", "")
            if not elem == "-":
                matrix[row_count, column_count] = int(elem)
            column_count += 1
        row_count += 1

    return matrix

file = "sudokus/puz-001.txt"

matrix = read_file(file)

print matrix


class Sudoku:


    B = range(0,9)
    I = range(0,3)
    b = [range(0,3), range(3,6), range(6,9)]

    def __init__(self, matrix):
        self.matrix = matrix


    def constraint_row(self, row, column, value):

        for elem in self.B:
            if row != elem:










