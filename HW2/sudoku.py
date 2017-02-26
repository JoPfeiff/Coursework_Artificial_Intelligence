import numpy as np
import copy
import itertools
import os
# import List


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
    D = range(1,10)

    def __init__(self, matrix, ac3, mvr):

        self.ac3 = ac3
        self.mvr = mvr
        self.matrix = matrix
        self.domain_dict = self.initialize_domain(self.matrix)

        self.depth = 0

        self.guess = 0



    def initialize_domain(self, matrix):
        domain_dict = {}
        for i in self.B:
            for j in self.B:
                if matrix[i,j] != 0:
                    domain_dict[str(i)+str(j)] = []
                else:
                    domain_dict[str(i)+str(j)] = self.D
        return domain_dict


    def update_domains(self, matrix, domain_dict):
        if self.ac3:
            for i in self.B:
                for j in self.B:
                    #if (i == 0 and j == 4):
                        #print "hi"
                    if matrix[i,j] == 0:
                        # if len(domain_dict[str(i)+str(j)]) == 1:
                        #     matrix[i,j] = domain_dict[str(i)+str(j)][0]
                        # elif len(domain_dict[str(i) + str(j)]) == 0:
                        #     return False
                        #
                        # else:
                        new_domain = []
                        for value in domain_dict[str(i)+str(j)]:
                            if self.check_constrainst(i, j, value, matrix):
                                new_domain.append(value)
                        if new_domain == []:
                            # print("error in %s %s, value = %s") %(i,j, domain_dict[str(i)+str(j)])
                            return False
                        domain_dict[str(i) + str(j)] = new_domain
        domain_dict = self.x_wing(domain_dict)
        return domain_dict

    def backtracking_search(self):
        new_domain_dict = self.update_domains(self.matrix, self.domain_dict)
        return self.recursive_backtracking(new_domain_dict,self.matrix, 0)

    def get_next_variable(self, matrix, domain_dict):
        if(self.mvr):
            min_length = 10
            best = None
            for key, value in domain_dict.items():
                length = len(value)
                if length == 1:
                    return int(key[0]), int(key[1])
                if (length > 0) and (length < min_length):
                    min_length = length
                    best = key
            return int(best[0]), int(best[1])
        else:
            for i in self.B:
                for j in self.B:
                    if matrix[i,j] == 0:
                        return i,j

    def x_wing(self, domain_dict):
        for r1 in self.B:
            for r2 in self.B:
                if r1 != r2:
                    for c1 in self.B:
                        for c2 in self.B:
                            if c1 != c2:
                                all_domains = set(domain_dict[str(r1) + str(c1)]) \
                                            | set(domain_dict[str(r1) + str(c2)]) \
                                            | set(domain_dict[str(r2) + str(c1)]) \
                                            | set(domain_dict[str(r2) + str(c2)])
                                #resultList = [1, 2, 5, 7, 9]
                                for domain in all_domains:
                                    if domain not in domain_dict[str(r1)+ str(c1)]:
                                        break
                                    if domain not in domain_dict[str(r1) + str(c2)]:
                                        break
                                    if domain not in domain_dict[str(r2) + str(c1)]:
                                        break
                                    if domain not in domain_dict[str(r2) + str(c2)]:
                                        break

                                    for row in [r1,r2]:
                                        for column in self.B:
                                            if column not in [c1,c2]:
                                                if domain in domain_dict[str(row) + str(column)]:
                                                    domain_dict[str(row) + str(column)].remove(domain)
                                    for column in [c1,c2]:
                                       for row in self.B:
                                           if row not in [r1,r2]:
                                               if domain in domain_dict[str(row) + str(column)]:
                                                   domain_dict[str(row) + str(column)].remove(domain)
        return domain_dict




    def get_best_next_variable(self, domain_dict):
        min_length = 10
        best = None
        for key, value in domain_dict.items():
            length = len(value)
            if length == 1 :
                return int(key[0]), int(key[1])
            if (length > 0) and (length < min_length):
                min_length = length
                best = key
        return int(best[0]), int(best[1])

    def get_nr_guesses(self):
        return self.guess

    def recursive_backtracking(self, domain_dict, matrix, depth):
        if not 0 in matrix:
            return matrix

        #print matrix

        i, j = self.get_next_variable(matrix, domain_dict)
        #i, j = self.get_best_next_variable(domain_dict)
        self.guess += len(domain_dict[str(i) + str(j)]) - 1
        for value in domain_dict[str(i)+str(j)]:

            # print ("depth = %s, length = %s" ) %(depth, len(domain_dict[str(i)+str(j)]))
            if self.check_constrainst(i,j,value,matrix):
                new_matrix , new_domain_dict = self.set_value(matrix, domain_dict, i,j,value)

                new_domain_dict = self.update_domains(new_matrix, new_domain_dict)
                if new_domain_dict is not False:
                    #return False
                    result =  self.recursive_backtracking(new_domain_dict,new_matrix, depth+1)

                    if result is not False:
                        return result

        return False

    def set_value(self,matrix, domain_dict, i,j,value):
        new_matrix = copy.deepcopy(matrix)
        new_domain_dict = copy.deepcopy(domain_dict)
        new_matrix[i,j] = value
        new_domain_dict[str(i)+str(j)] = []
        return new_matrix, new_domain_dict

    def check_constrainst(self, row_elem, column_elem, value, matrix):
        # print (self.constraint_row(row_elem,column_elem,value, matrix))
        # print self.constraint_column(row_elem,column_elem,value, matrix)
        # print self.constraint_square(row_elem, column_elem, value, matrix)
        # print (self.constraint_row(row_elem,column_elem,value, matrix) and self.constraint_column(row_elem,column_elem,value, matrix)) and self.constraint_square(row_elem, column_elem, value, matrix)
        # print("\n")

        return (self.constraint_row(row_elem,column_elem,value, matrix) and self.constraint_column(row_elem,column_elem,value, matrix)) and self.constraint_square(row_elem, column_elem, value, matrix)

    def constraint_row(self, row_elem, column_elem, value, matrix):
        for row_compare in self.B:
            if row_elem != row_compare:
                #compare_value = matrix[column_elem, row_compare]
                test = matrix[row_compare, column_elem]
                if(matrix[row_compare, column_elem] == value):
                    return False
        return True


    def constraint_column(self, row_elem, column_elem, value, matrix):
        for column_compare in self.B:
            if column_elem != column_compare:
                #compare_value = self.matrix[column_compare, row_elem]
                if (matrix[row_elem, column_compare] == value):
                    return False
        return True

    def constraint_square(self, row_elem, column_elem, value, matrix):
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
                    #compare_value = matrix[column_compare, row_compare]
                    if (matrix[row_compare, column_compare] == value):
                        return False
        return True


#file = "sudokus/puz-001_solved_missing.txt"

for file in os.listdir("sudokus/"):
    if file.endswith(".txt"):
        #file = "sudokus/puz-001.txt"

        matrix = read_file("sudokus/"+file)

        sudoku = Sudoku(matrix, True, True)
        sudoku.backtracking_search()
        print("File %s: nr of guesses = %s") %(file, sudoku.get_nr_guesses())
        #print sudoku.get_nr_guesses()

#print matrix

