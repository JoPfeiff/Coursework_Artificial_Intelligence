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

    def __init__(self, matrix, ac3 = True, mrv = True, xwing = True, custom_inference = True, naked_pair_inference=True):

        self.ac3 = ac3
        self.mrv = mrv
        self.xwing = xwing
        self.custom_inference = custom_inference
        self.naked_pair_inference= naked_pair_inference
        self.matrix = matrix
        self.domain_dict = self.initialize_domain(self.matrix)
        self.depth = 0
        self.guess = 0

################################################################################################################################################################################
################################################################################################################################################################################
    # This part has the initialisation of domain, the waterfall call and the recursive backtrack algorithm #


    def initialize_domain(self, matrix):
        domain_dict = {}
        for i in self.B:
            for j in self.B:
                if matrix[i,j] != 0:
                    domain_dict[str(i)+str(j)] = []
                else:
                    domain_dict[str(i)+str(j)] = copy.deepcopy(self.D)
        return domain_dict



    def update_domains(self, matrix, domain_dict):
        if self.ac3:
            domain_dict=self.ac3_newest(matrix, domain_dict)
            if domain_dict is False:
                return False
        if self.custom_inference:
            domain_dict = self.custom_inference_method(matrix, domain_dict)
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

    def recursive_backtracking(self, domain_dict, matrix, depth):

        if not 0 in matrix:
            return matrix

        i, j = self.get_next_variable(matrix, domain_dict)

        self.guess += len(domain_dict[str(i) + str(j)]) - 1
        for value in domain_dict[str(i) + str(j)]:

            if self.check_constraint(i,j,value,matrix):
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

    def get_nr_guesses(self):
        return self.guess

################################################################################################################################################################################
################################################################################################################################################################################
    # This part has the constraints #


    def check_constraint(self, row_elem, column_elem, value, matrix):
        return (self.constraint_row(row_elem,column_elem,value, matrix) and self.constraint_column(row_elem,column_elem,value, matrix)) and self.constraint_square(row_elem, column_elem, value, matrix)

    def constraint_row(self, row_elem, column_elem, value, matrix):
        for row_compare in self.B:
            if row_elem != row_compare:
                if (matrix[row_compare, column_elem] == value):
                    return False
        return True


    def constraint_column(self, row_elem, column_elem, value, matrix):
        for column_compare in self.B:
            if column_elem != column_compare:
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



################################################################################################################################################################################
################################################################################################################################################################################
    # This part has the MRV implementation #


    def get_next_variable(self, matrix, domain_dict):
        if(self.mrv):
            min_length = float('inf')
            best = None
            for key, value in sorted(domain_dict.items()):
                if matrix[int(key[0]),int(key[1])] != 0:
                    continue 

                length=0
                for i in value:
                    length += int(self.check_constraint(int(key[0]), int(key[1]), i, matrix))

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




 ################################################################################################################################################################################
 ################################################################################################################################################################################
    # This part has the AC3 algorithm #



    def get_arcs(self,matrix,domain_dict):
        arcs=[]
        keys=domain_dict.keys()
        starting_squares= [i for i in keys if matrix[int(i[0]),int(i[1])] == 0]
        ending_squares=[i for i in keys]        
        for starting_square in starting_squares:
            for ending_square in ending_squares:
                if starting_square!=ending_square and self.is_neighbouring(starting_square,ending_square):
                    arcs.append((starting_square,ending_square))
        return arcs

    def ac3_newest(self, matrix,domain_dict):
        arcs=self.get_arcs(matrix,domain_dict)
        while arcs:
            start_var,end_var=arcs.pop(0)
            if self.revise(domain_dict, matrix, start_var, end_var):
                if not domain_dict[start_var]:
                    return False
                if len(domain_dict[start_var]) == 1:
                    matrix[int(start_var[0]), int(start_var[1])] = domain_dict[start_var][0]
                    domain_dict[start_var] = []
                neighbours = self.get_neighbours(start_var,domain_dict)
                for neighbour in neighbours:
                     if end_var != neighbour:
                        arcs.append((neighbour, start_var))
        return domain_dict

    def revise(self,domain_dict, matrix,start_var,end_var):
        revised = False
        for value in domain_dict[start_var]:
            end_domain = domain_dict[end_var]
            if (value not in end_domain) and (matrix[int(end_var[0]) , int(end_var[1])] != value):
                continue
            if len(end_domain)==1:
                domain_dict[start_var].remove(value)
                revised = True
            if (matrix[int(end_var[0]), int(end_var[1])] == value):
                domain_dict[start_var].remove(value)
                revised = True
        return revised


    def get_neighbours(self,cell,domain_dict):
        keys=domain_dict.keys()
        neighbours = []
        ending_squares=[i for i in keys]
        for ending_square in ending_squares:
            if cell!=ending_square and self.is_neighbouring(cell,ending_square):
                neighbours.append(ending_square)
        return neighbours


    def is_neighbouring(self,cell1,cell2):
        same_box_row = False
        same_box_column = False
        for box in self.b:
            if (cell1[0] in box) and (cell2[0] in box):
                same_box_row = True
            if (cell1[1] in box) and (cell2[1] in box):
               same_box_column = True

        if cell1[0]==cell2[0] or cell1[1]==cell2[1] or (same_box_column and same_box_row):
            return True

################################################################################################################################################################################
################################################################################################################################################################################
    # This part has the custom inference algorithm #


    def custom_inference_method(self,  matrix, domain_dict):
        for i in self.B:
            for j in self.B:
                if matrix[i, j] == 0:
                    new_domain = []
                    for value in domain_dict[str(i) + str(j)]:
                        if self.check_constraint(i, j, value, matrix):
                            new_domain.append(value)
                    if new_domain == []:
                        # print("error in %s %s, value = %s") %(i,j, domain_dict[str(i)+str(j)])
                        return False
                    domain_dict[str(i) + str(j)] = new_domain
        return domain_dict



################################################################################################################################################################################
################################################################################################################################################################################
    # This part has the xwing inference algorithm #


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
                                for domain in all_domains:
                                    if (domain not in domain_dict[str(r1)+ str(c1)]) and (not self.check_constraint(r1, c1, domain, matrix)):
                                        break
                                    if (domain not in domain_dict[str(r1) + str(c2)])  and (not self.check_constraint(r1, c2, domain, matrix)):
                                        break
                                    if (domain not in domain_dict[str(r2) + str(c1)]) and (not self.check_constraint(r2, c1, domain, matrix)):
                                        break
                                    if (domain not in domain_dict[str(r2) + str(c2)])  and (not self.check_constraint(r2, c2, domain, matrix)):
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

        return domain_dict

################################################################################################################################################################################
################################################################################################################################################################################
    # This part has the Naked Pairs algorithm #



    def get_naked_pairs(self,domain_dict):
        pairs=[]

        potential_np=self.get_potential_np(domain_dict)
        for start_np in potential_np:
            for end_np in potential_np:
                if start_np==end_np:
                    continue

                if not self.is_neighbouring(start_np,end_np):
                    continue
                start_dom_naked=domain_dict[start_np]
                end_dom_naked=domain_dict[end_np]

                if start_dom_naked!=end_dom_naked:
                    continue

                naked_pair=(start_np,end_np)
                reversed_naked_pair=(end_np,start_np)

                if naked_pair not in pairs and reversed_naked_pair not in pairs:
                    pairs.append(naked_pair)
        return pairs

    def get_potential_np(self,domain_dict):
        potential_np=[]
        for i in domain_dict.keys():
             potential_pair = domain_dict[i]
             if len(potential_pair) == 2:
                potential_np.append(i)
        return potential_np

    def naked_pairs(self, domain_dict, matrix):
        pairs=self.get_naked_pairs(domain_dict)
        for start_np, end_np in pairs:
            dom_naked = domain_dict[start_np]
            neighbours_of_start = self.get_neighbours(start_np,domain_dict)
            neighbours_of_end = self.get_neighbours(end_np,domain_dict)
            neighbours = list(set(neighbours_of_start) & set(neighbours_of_end))
            for x in neighbours:
                neighbour_domain=domain_dict[x]
                for value in dom_naked:
                    if value in neighbour_domain:
                        neighbour_domain.remove(value)
                        if not neighbour_domain:
                             return False
        return domain_dict




################################################################################################################################################################################
################################################################################################################################################################################
    # This part runs everything #


for file in os.listdir("sudokus/"):
    if file.endswith(".txt"):
        #file = "sudokus/puz-001.txt"

        matrix = read_file("sudokus/"+file)

        sudoku1 = Sudoku(matrix, ac3 = False, xwing=False, mrv = False, custom_inference = False, naked_pair_inference=False)
        matrix1 = sudoku1.backtracking_search()
        if(matrix1 is False):
            print "False"
        print("File %s: nr of Naive guesses = %s") %(file, sudoku1.get_nr_guesses())

        sudoku2 = Sudoku(matrix, ac3 = False, xwing=False, mrv = True,  custom_inference = False, naked_pair_inference=False)
        matrix2 = sudoku2.backtracking_search()
        if(matrix2 is False):
            print "False"
        print("File %s: nr of MRV guesses = %s") %(file, sudoku2.get_nr_guesses())

        
        sudoku3 = Sudoku(matrix, ac3 = True, xwing=False, mrv = False, custom_inference = False,naked_pair_inference=False)
        matrix3 = sudoku3.backtracking_search()
        if(matrix3 is False):
            print "False"
        print("File %s: nr of AC3 w/o MRV guesses = %s ") %(file, sudoku3.get_nr_guesses())

        sudoku3 = Sudoku(matrix, ac3 = True, xwing=False, mrv = True, custom_inference = False,naked_pair_inference=False)
        matrix3 = sudoku3.backtracking_search()
        if(matrix3 is False):
            print "False"
        print("File %s: nr of AC3 w/ MRV guesses = %s ") %(file, sudoku3.get_nr_guesses())
        
        
        
        sudoku4 = Sudoku(matrix, ac3=True, xwing=False, mrv=True, custom_inference=True,naked_pair_inference=False)
        matrix4 = sudoku4.backtracking_search()
        if (matrix4 is False):
            print "False"
        print("File %s: nr of AC3 and MRV and custom_inference guesses = %s") % (file, sudoku4.get_nr_guesses())
        
        sudoku5 = Sudoku(matrix, ac3=True, xwing=True, mrv=True, custom_inference=True,naked_pair_inference=False)
        matrix5 = sudoku5.backtracking_search()
        if (matrix5 is False):
            print "False"
        print("File %s: nr of AC3 and MRV and custom_inference and XWing guesses = %s") % (file, sudoku5.get_nr_guesses())

        sudoku6 = Sudoku(matrix, ac3=True, xwing=True, mrv=True, custom_inference=True,naked_pair_inference=True)
        matrix6 = sudoku6.backtracking_search()
        if (matrix6 is False):
            print "False"
        print("File %s: nr of AC3 and MRV and custom_inference and XWing and naked pairs guesses = %s") % (file, sudoku6.get_nr_guesses())

        print " "

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
