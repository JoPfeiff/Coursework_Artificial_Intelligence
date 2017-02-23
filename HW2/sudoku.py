import numpy as np
import copy
import itertools


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

    def __init__(self, matrix):
        self.matrix = matrix
        self.domain_dict = self.initialize_domain(self.matrix)

        self.depth = 0

        self.guess = 0

        print "done"


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

        return domain_dict

    def backtracking_search(self):
        ##############
        # forward selection
        ##################
        new_domain_dict = self.update_domains(self.matrix, self.domain_dict)

        ##############
        # NO forward selection
        ##################
        #new_domain_dict = self.domain_dict


        return self.recursive_backtracking(new_domain_dict,self.matrix, 0)

    def get_next_variable(self, matrix):
        for i in self.B:
            for j in self.B:
                if matrix[i,j] == 0:
                    return i,j

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


        #i, j = self.get_next_variable(matrix)
        i, j = self.get_best_next_variable(domain_dict)
        self.guess += len(domain_dict[str(i) + str(j)]) - 1
        for value in domain_dict[str(i)+str(j)]:

            # print ("depth = %s, length = %s" ) %(depth, len(domain_dict[str(i)+str(j)]))
            if self.check_constrainst(i,j,value,matrix):
                new_matrix , new_domain_dict = self.set_value(matrix, domain_dict, i,j,value)

                ##############
                # forward selection
                ##################
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
file = "sudokus/puz-100.txt"

matrix = read_file(file)

sudoku = Sudoku(matrix)
print sudoku.backtracking_search()
print sudoku.get_nr_guesses()

#print matrix

