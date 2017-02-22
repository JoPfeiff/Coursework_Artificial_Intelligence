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




class Sudoku:


    B = range(0,9)
    I = range(0,3)
    b = [range(0,3), range(3,6), range(6,9)]

    def __init__(self, matrix):
        self.matrix = matrix

        row_elem = 1
        column_elem = 1
        value = 8

        row_test = self.constraint_row(row_elem,column_elem,value)
        column_test = self.constraint_column(row_elem,column_elem,value)
        square_test = self.constraint_square(row_elem,column_elem,value)
        print "done"


    def constraint_row(self, row_elem, column_elem, value):
        for row_compare in self.B:
            if row_elem != row_compare:
                compare_value = self.matrix[column_elem, row_compare]
                if(self.matrix[column_elem, row_compare] == value):
                    return False
        return True


    def constraint_column(self, row_elem, column_elem, value):
        for column_compare in self.B:
            if column_elem != column_compare:
                compare_value = self.matrix[column_compare, row_elem]
                if (self.matrix[column_compare, row_elem] == value):
                    return False
        return True

    def constraint_square(self, row_elem, column_elem, value):
        b1 = []
        b2 = []
        for box in self.b:
            if row_elem in box:
                b1 = box
            if column_elem in box:
                b2 = box

        for row_compare in b1:
            for column_compare in b2:
                if not( (row_elem == row_compare) & (column_elem == column_compare)):
                    compare_value = self.matrix[column_compare, row_compare]
                    if (self.matrix[column_compare, row_compare] == value):
                        return False
        return True


file = "sudokus/puz-001.txt"

matrix = read_file(file)

sudoku = Sudoku(matrix)

print matrix

