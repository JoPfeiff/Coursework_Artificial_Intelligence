import numpy as np
import copy
import itertools
import os
# import List
import time


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

    def __init__(self, matrix, ac3 = True, mvr = True, xwing = True, ac3J = True, naked_pair_inference=True):

        self.ac3 = ac3
        self.mvr = mvr
        self.xwing = xwing
        self.ac3J = ac3J
        self.naked_pair_inference= naked_pair_inference
        self.matrix = matrix
        self.domain_dict = self.initialize_domain(self.matrix)

        self.depth = 0

        self.guess = 0

    def get_arcs(self,matrix,domain_dict):
        arcs=[]
        keys=domain_dict.keys()
        start_cells= [i for i in keys if matrix[int(i[0]),int(i[1])] == 0]
        end_cells=[i for i in keys]

        
        for start_cell in start_cells:
            for end_cell in end_cells:
                if start_cell!=end_cell and self.isNeighbour(start_cell,end_cell):
                    arcs.append((start_cell,end_cell))
        return arcs

    def ac3_newest(self, matrix,domain_dict):
        arcs=self.get_arcs(matrix,domain_dict)
        while arcs:
            start_variable,end_variable=arcs.pop(0)
            if self.revise(domain_dict, matrix, start_variable, end_variable):


                if not domain_dict[start_variable]:
                    return False

                if len(domain_dict[start_variable]) == 1:
                    matrix[int(start_variable[0]), int(start_variable[1])] = domain_dict[start_variable][0]
                    domain_dict[start_variable] = []

                neighbors = self.getNeighbour(start_variable,domain_dict)
                for neighbor in neighbors:
                     if end_variable != neighbor:
                        arcs.append((neighbor, start_variable))
        return domain_dict

    def revise(self,domain_dict, matrix,start_variable,end_variable):
        is_revised = False
        for value in domain_dict[start_variable]:
            end_domain = domain_dict[end_variable]
            if (value not in end_domain) and (matrix[int(end_variable[0]) , int(end_variable[1])] != value):
                continue
            if len(end_domain)==1:
                domain_dict[start_variable].remove(value)
                is_revised = True

            if (matrix[int(end_variable[0]), int(end_variable[1])] == value):

                domain_dict[start_variable].remove(value)
                is_revised = True

            # if len(domain_dict[start_variable]) == 1:
            #     matrix[start_variable[0], start_variable[1]] = domain_dict[start_variable][0]
            #     domain_dict[start_variable] = []

        return is_revised


    def getNeighbour(self,cell,domain_dict):
        keys=domain_dict.keys()
        neighbors = []
        end_cells=[i for i in keys]
        for end_cell in end_cells:
            if cell!=end_cell and self.isNeighbour(cell,end_cell):
                neighbors.append(end_cell)
        return neighbors


    def isNeighbour(self,cell1,cell2):
        same_box_row = False
        same_box_column = False
        for box in self.b:
            if (cell1[0] in box) and (cell2[0] in box):
                same_box_row = True
            if (cell1[1] in box) and (cell2[1] in box):
               same_box_column = True

        if cell1[0]==cell2[0] or cell1[1]==cell2[1] or (same_box_column and same_box_row):
            return True


    def get_naked_pairs(self,domain_dict):
        pairs=[]

        potential_naked_pairs=self.get_potential_naked_pairs(domain_dict)
        for start_naked_pair in potential_naked_pairs:
            for end_naked_pair in potential_naked_pairs:
                if start_naked_pair==end_naked_pair:
                    continue

                if not self.isNeighbour(start_naked_pair,end_naked_pair):
                    continue
                start_naked_domain=domain_dict[start_naked_pair]
                end_naked_domain=domain_dict[end_naked_pair]

                if start_naked_domain!=end_naked_domain:
                    continue

                naked_pair=(start_naked_pair,end_naked_pair)
                inverted_naked_pair=(end_naked_pair,start_naked_pair)

                if naked_pair not in pairs and inverted_naked_pair not in pairs:
                    pairs.append(naked_pair)
        return pairs

    def get_potential_naked_pairs(self,domain_dict):
        potential_naked_pairs=[]
        for i in domain_dict.keys():
             potential_pair = domain_dict[i]
             if len(potential_pair) == 2:
                potential_naked_pairs.append(i)
        return potential_naked_pairs

    def naked_pairs(self, domain_dict, matrix):
        pairs=self.get_naked_pairs(domain_dict)
        for start_naked_pair, end_naked_pair in pairs:
            naked_domain = domain_dict[start_naked_pair]

            start_neighbors = self.getNeighbour(start_naked_pair,domain_dict)
            end_neighbors = self.getNeighbour(end_naked_pair,domain_dict)
            neighbors = list(set(start_neighbors) & set(end_neighbors))

            for x in neighbors:
                neighbor_domain=domain_dict[x]
                for value in naked_domain:
                    if value in neighbor_domain:
                        neighbor_domain.remove(value)
                        if not neighbor_domain:
                             return False
        return domain_dict



    def initialize_domain(self, matrix):
        domain_dict = {}
        for i in self.B:
            for j in self.B:
                if matrix[i,j] != 0:
                    domain_dict[str(i)+str(j)] = []
                else:
                    domain_dict[str(i)+str(j)] = copy.deepcopy(self.D)
        return domain_dict

    def ac3_algo(self,  matrix, domain_dict):
        for i in self.B:
            for j in self.B:
                if matrix[i, j] == 0:
                    new_domain = []
                    for value in domain_dict[str(i) + str(j)]:
                        if self.check_constrainst(i, j, value, matrix):
                            new_domain.append(value)
                    if new_domain == []:
                        # print("error in %s %s, value = %s") %(i,j, domain_dict[str(i)+str(j)])
                        return False
                    domain_dict[str(i) + str(j)] = new_domain
        return domain_dict

    def ac3_algo_new(self, matrix, domain_dict):
        queue = []
        for item in domain_dict.items():
            queue.append([item])

        while len(queue) > 0:
            print(" ")

    def update_domains(self, matrix, domain_dict):
        if self.ac3J:
            domain_dict = self.ac3_algo(matrix, domain_dict)
            if domain_dict is False:
                return False
        if self.ac3:
            domain_dict=self.ac3_newest(matrix, domain_dict)
            if domain_dict is False:
                return False
        if self.xwing:
            domain_dict = self.x_wing(domain_dict, matrix)
            if domain_dict is False:
                return False
        if self.naked_pair_inference:
            domain_dict=self.naked_pairs(domain_dict,matrix)
            if domain_dict is False:
                return False

        return domain_dict

    def backtracking_search(self):
        
        new_domain_dict = self.update_domains(self.matrix, self.domain_dict)
        return self.recursive_backtracking(new_domain_dict,self.matrix, 0)

    def get_next_variable(self, matrix, domain_dict):
        # print matrix

        if(self.mvr):
            min_length = float('inf')
            best = None
            for key, value in sorted(domain_dict.items()):
                if matrix[int(key[0]),int(key[1])] != 0:
                    continue 

                length=0
                for i in value:
                    length += int(self.check_constrainst(int(key[0]), int(key[1]), i, matrix))

                if length < min_length:
                    min_length = length
                    best = key
            if best is None:
                for i in self.B:
                    for j in self.B:
                        if matrix[i,j] == 0:
                            return i,j

            return int(best[0]), int(best[1])
        else:
            for i in self.B:
                for j in self.B:
                    if matrix[i,j] == 0:
                        return i,j

    def x_wing(self, domain_dict, matrix):
        start = time.time()
        if domain_dict is False:
            return domain_dict
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
                                    if (domain not in domain_dict[str(r1)+ str(c1)]) and (not self.check_constrainst(r1, c1, domain, matrix)):
                                        break
                                    if (domain not in domain_dict[str(r1) + str(c2)])  and (not self.check_constrainst(r1, c2, domain, matrix)):
                                        break
                                    if (domain not in domain_dict[str(r2) + str(c1)]) and (not self.check_constrainst(r2, c1, domain, matrix)):
                                        break
                                    if (domain not in domain_dict[str(r2) + str(c2)])  and (not self.check_constrainst(r2, c2, domain, matrix)):
                                        break

                                    row_xwing = True
                                    for row in [r1,r2]:
                                        if row_xwing == True:

                                            for column in self.B:
                                                if column not in [c1,c2]:
                                                    if(domain in domain_dict[str(row) + str(column)]):
                                                        row_xwing = False
                                                        break
                                        else:
                                            break

                                    if row_xwing:
                                        for column in [c1, c2]:
                                            for row in self.B:
                                                if row not in [r1, r2]:
                                                    if domain in domain_dict[str(row) + str(column)]:
                                                        domain_dict[str(row) + str(column)].remove(domain)

                                    column_xwing = True
                                    for column in [c1,c2]:
                                        if column_xwing == True:
                                            for row in self.B:
                                                if row not in [r1,r2]:
                                                    if(domain in domain_dict[str(row) + str(column)]):
                                                        column_xwing = False
                                                        break
                                        else:
                                            break

                                    if column_xwing:
                                        for row in [r1, r2]:
                                            for column in self.B:
                                                if column not in [c1, c2]:
                                                    if domain in domain_dict[str(row) + str(column)]:
                                                        domain_dict[str(row) + str(column)].remove(domain)



                                    # for row in [r1,r2]:
                                    #     for column in self.B:
                                    #         if column not in [c1,c2]:
                                    #             if domain in domain_dict[str(row) + str(column)]:
                                    #                 domain_dict[str(row) + str(column)].remove(domain)
                                    # for column in [c1,c2]:
                                    #    for row in self.B:
                                    #        if row not in [r1,r2]:
                                    #            if domain in domain_dict[str(row) + str(column)]:
                                    #                domain_dict[str(row) + str(column)].remove(domain)

        #print "Time = %s" %(time.time()-start)
        return domain_dict




    # def get_best_next_variable(self, domain_dict):
    #     min_length = 10
    #     best = None
    #     for key, value in domain_dict.items():
    #         length = len(value)
    #         if length == 1 :
    #             return int(key[0]), int(key[1])
    #         if (length > 0) and (length < min_length):
    #             min_length = length
    #             best = key
    #     return int(best[0]), int(best[1])

    def get_nr_guesses(self):
        return self.guess

    def recursive_backtracking(self, domain_dict, matrix, depth):
        # print matrix
        if not 0 in matrix:
            return matrix

        #print matrix

        i, j = self.get_next_variable(matrix, domain_dict)

        #i, j = self.get_best_next_variable(domain_dict)

        # print domain_dict[str(i) + str(j)]
        self.guess += len(domain_dict[str(i) + str(j)]) - 1
        for value in domain_dict[str(i) + str(j)]:

            # print ("depth = %s, length = %s" ) %(depth, len(domain_dict[str(i)+str(j)]))
            if self.check_constrainst(i,j,value,matrix):
                new_matrix, new_domain_dict = self.set_value(matrix, domain_dict, i,j,value)

                new_domain_dict = self.update_domains(new_matrix, new_domain_dict)
                if new_domain_dict is not False:
                    result = self.recursive_backtracking(new_domain_dict,new_matrix, depth+1)

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
        return (self.constraint_row(row_elem,column_elem,value, matrix) and self.constraint_column(row_elem,column_elem,value, matrix)) and self.constraint_square(row_elem, column_elem, value, matrix)

    def constraint_row(self, row_elem, column_elem, value, matrix):
        for row_compare in self.B:
            if row_elem != row_compare:
                #compare_value = matrix[column_elem, row_compare]
                # test = matrix[row_compare, column_elem]
                if (matrix[row_compare, column_elem] == value):
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
                if not( (row_elem == row_compare) and (column_elem == column_compare)):
                    #compare_value = matrix[column_compare, row_compare]
                    if (matrix[row_compare, column_compare] == value):
                        return False
        return True
#f

#file = "sudokus/puz-001_solved_missing.txt"

# file = "empty.txti"
# #
# matrix = read_file("sudokus/"+file)
# sudoku = Sudoku(matrix, ac3 = True, xwing=False, mvr = True)
# matrix = sudoku.backtracking_search()
# print(matrix)
# print("File %s: nr of MRV guesses = %s\n") %(file, sudoku.get_nr_guesses())
for file in os.listdir("sudokus/"):
    if file.endswith(".txt"):
        #file = "sudokus/puz-001.txt"

        matrix = read_file("sudokus/"+file)

        # sudoku1 = Sudoku(matrix, ac3 = True, xwing=True, mvr = True, ac3J = True, naked_pair_inference=False)
        # matrix1 = sudoku1.backtracking_search()
        # if(matrix1 is False):
        #     print "False"
        # print("File %s: nr of Naive guesses = %s") %(file, sudoku1.get_nr_guesses())
        #
        # sudoku2 = Sudoku(matrix, ac3 = True, xwing=True, mvr = True,  ac3J = True, naked_pair_inference=True)
        # matrix2 = sudoku2.backtracking_search()
        # if(matrix2 is False):
        #     print "False"
        # print("File %s: nr of MRV guesses = %s") %(file, sudoku2.get_nr_guesses())

        #
        # sudoku3 = Sudoku(matrix, ac3 = True, xwing=False, mvr = True, ac3J = False)
        # matrix3 = sudoku3.backtracking_search()
        # if(matrix3 is False):
        #     print "False"
        # print("File %s: nr of AC3 and MRV guesses = %s ") %(file, sudoku3.get_nr_guesses())

        # sudoku3 = Sudoku(matrix, ac3 = True, xwing=False, mvr = True, ac3J = False)
        # matrix3 = sudoku3.backtracking_search()
        # if(matrix3 is False):
        #     print "False"
        # print("File %s: nr of AC3 and MRV guesses = %s ") %(file, sudoku3.get_nr_guesses())
        #
        #
        #
        # sudoku4 = Sudoku(matrix, ac3=True, xwing=False, mvr=True, ac3J=True)
        # matrix4 = sudoku4.backtracking_search()
        # if (matrix4 is False):
        #     print "False"
        # print("File %s: nr of AC3 and MRV and AC3J guesses = %s") % (file, sudoku4.get_nr_guesses())
        #
        # sudoku5 = Sudoku(matrix, ac3=True, xwing=True, mvr=True, ac3J=True)
        # matrix5 = sudoku5.backtracking_search()
        # if (matrix5 is False):
        #     print "False"
        # print("File %s: nr of AC3 and MRV and AC3J and XWing guesses = %s") % (file, sudoku5.get_nr_guesses())



        # print("")
#print matrix

# File puz-001.txt: nr of AC3 guesses = 0
# File puz-002.txt: nr of AC3 guesses = 0
# File puz-010.txt: nr of AC3 guesses = 0
# File puz-015.txt: nr of AC3 guesses = 0
# File puz-025.txt: nr of AC3 guesses = 1
# File puz-026.txt: nr of AC3 guesses = 21
# File puz-048.txt: nr of AC3 guesses = 8
# File puz-051.txt: nr of AC3 guesses = 10
# File puz-062.txt: nr of AC3 guesses = 2
# File puz-076.txt: nr of AC3 guesses = 6
# File puz-081.txt: nr of AC3 guesses = 10
# File puz-082.txt: nr of AC3 guesses = 5
# File puz-090.txt: nr of AC3 guesses = 6
# File puz-095.txt: nr of AC3 guesses = 11
# File puz-099.txt: nr of AC3 guesses = 9
# File puz-100.txt: nr of AC3 guesses = 9


# File puz-001.txt: nr of guesses = 0
#
# File puz-001_solved.txt: nr of guesses = 0
#
# File puz-001_solved_missing.txt: nr of guesses = 0
#
# File puz-002.txt: nr of guesses = 0
#
# File puz-010.txt: nr of guesses = 0
#
# File puz-015.txt: nr of guesses = 0
#
# File puz-025.txt: nr of guesses = 0
#
# File puz-026.txt: nr of guesses = 22
#
# File puz-048.txt: nr of guesses = 6
#
# File puz-051.txt: nr of guesses = 2
#
# File puz-062.txt: nr of guesses = 10
#
# File puz-076.txt: nr of guesses = 6
#
# File puz-081.txt: nr of guesses = 5
#
# File puz-082.txt: nr of guesses = 22
#
# File puz-090.txt: nr of guesses = 25
#
# File puz-095.txt: nr of guesses = 28
#
# File puz-099.txt: nr of guesses = 13
#
# File puz-100.txt: nr of guesses = 6
