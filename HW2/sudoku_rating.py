import os
from sudoku_final import Sudoku
import numpy as np
from sklearn.metrics import mean_squared_error


from sklearn.linear_model import LinearRegression

def rmse(predictions, targets):
    return np.sqrt(mean_squared_error(predictions, targets))






def gen_test_data(directory):

    data = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            puzzle = read_test_file(directory+file)
            label = get_test_label(file)
            data.append(get_row(puzzle,label))

    #print data
    data = np.array(data)
    return data[:, 0:data.shape[1] - 1] , data[:,-1]


def gen_data(directory):
    max_files = 10
    data = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            with open(directory + "/" + file) as f:
                content = f.readlines()
            nr = 0
            for line in content:
                if nr == max_files: break
                nr += 1
                puzzle = read_line(line)
                label = get_label(file)
                data.append(get_row(puzzle,label))

    #print data
    data = np.array(data)
    return data[:, 0:data.shape[1] - 1] , data[:,-1]


def read_line(line):
    array= []
    for i in range(0,len(line)):
        try:
            array.append(int(line[i]))
        except:
            break

    array = np.array(array)
    array = array.reshape(9,9)
    return array


def read_test_file(file_name):
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

def get_test_label(file_name):
    return int(file_name[4:-4])

def get_label(file_name):
    return int(file_name[:-4])


def get_row(puzzle, label):
    # sud_guess = Sudoku(puzzle, ac3=False, xwing=False, mvr=False, ac3J=False)
    # sud_guess.backtracking_search()
    # guess = sud_guess.get_nr_guesses()
    sud_ac3 = Sudoku(puzzle,  ac3 = True, xwing=False, mrv = False, custom_inference = False, naked_pair_inference=False)
    sud_ac3.backtracking_search()
    ac3 = sud_ac3.get_nr_guesses()
    sud_mrv = Sudoku(puzzle,  ac3 = True, xwing=False, mrv = True, custom_inference = False, naked_pair_inference=False)
    sud_mrv.backtracking_search()
    mrv = sud_mrv.get_nr_guesses()
    sud_ac3j = Sudoku(puzzle,  ac3 = True, xwing=False, mrv = True, custom_inference = True, naked_pair_inference=False)
    sud_ac3j.backtracking_search()
    ac3j = sud_ac3j.get_nr_guesses()
    sud_xwing = Sudoku(puzzle,  ac3 = True, xwing=True, mrv = True, custom_inference = True, naked_pair_inference=False)
    sud_xwing.backtracking_search()
    xwing = sud_xwing.get_nr_guesses()
    sud_naked = Sudoku(puzzle,  ac3 = True, xwing=True, mrv = True, custom_inference = True, naked_pair_inference=True)
    sud_naked.backtracking_search()
    naked = sud_naked.get_nr_guesses()

    row = [ac3,mrv,ac3j,xwing, naked,label]
    #print row
    return row


def fit_predict():
    train_x, train_y = gen_data("sudoku_training/")

    test_x , test_y = gen_test_data("sudokus/")

    classifier = LinearRegression()
    classifier.fit(train_x,train_y)
    prediction = classifier.predict(test_x)
    print prediction
    print rmse(prediction, test_y)


fit_predict()