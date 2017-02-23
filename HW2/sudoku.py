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
    D = range(1,10)

    def __init__(self, matrix):
        self.matrix = matrix
        self.domain_dict = self.initialize_domain(self.matrix)



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
                    domain_dict[str(i) + str(j)] = new_domain

        return domain_dict

    def backtracking_search(self):

        return self.recursive_backtracking(self.domain_dict,self.matrix)

    def get_next_variable(self, matrix):
        for i in self.B:
            for j in self.B:
                if matrix[i,j] == 0:
                    return i,j

    def recursive_backtracking(self, domain_dict, matrix):
        if not 0 in matrix:
            return matrix

        # put unassigned variable here
        domain_dict = self.update_domains(matrix, domain_dict)
        i, j = self.get_next_variable(matrix)

        print "%s%s" %(i,j)

        if (i == 8) and (j == 8):
            print "here"
        for value in domain_dict[str(i)+str(j)]:
            if self.check_constrainst(i,j,value,matrix):
                new_matrix = copy.copy(matrix)
                new_matrix[i,j] = value
                new_domain_dict = copy.copy(domain_dict)
                new_domain_dict[str(i)+str(j)] = []
                new_domain_dict = self.update_domains(new_matrix,new_domain_dict)
                if 0 not in new_matrix:
                    return matrix
                result =  self.recursive_backtracking(new_domain_dict,new_matrix)
                #print result

                # if result is False:
                #     print "\n"
                #     print matrix

                if result is not False:
                    return result

        return False


    def check_constrainst(self, row_elem, column_elem, value, matrix):
        return (self.constraint_row(row_elem,column_elem,value, matrix) and self.constraint_column(row_elem,column_elem,value, matrix)) and self.constraint_square(row_elem, column_elem, value, matrix)

    def constraint_row(self, row_elem, column_elem, value, matrix):
        for row_compare in self.B:
            if row_elem != row_compare:
                #compare_value = matrix[column_elem, row_compare]
                if(matrix[column_elem, row_compare] == value):
                    return False
        return True


    def constraint_column(self, row_elem, column_elem, value, matrix):
        for column_compare in self.B:
            if column_elem != column_compare:
                #compare_value = self.matrix[column_compare, row_elem]
                if (matrix[column_compare, row_elem] == value):
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
                    if (matrix[column_compare, row_compare] == value):
                        return False
        return True


#file = "sudokus/puz-001_solved_missing.txt"
file = "sudokus/puz-001.txt"

matrix = read_file(file)

sudoku = Sudoku(matrix)
print sudoku.backtracking_search()

#print matrix

