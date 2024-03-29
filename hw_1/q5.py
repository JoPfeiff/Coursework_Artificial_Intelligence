

import collections
from operator import itemgetter
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import time

class Node():

    parent_node = None
    cost = 999999999999999

    def __init__(self, node_name, child_node_names):
        self.node_name = node_name
        #self.parent_node_name = parent_node_name
        #self.child_node_names = {}
        self.child_node_names = child_node_names


    def set_parent(self, parent_node):
        self.parent_node = parent_node

    def set_cost(self, cost):
        self.cost = cost

    def get_parent(self):
        return self.parent_node

    def get_cost(self):
        return  self.cost

    def get_children(self):
        return self.child_node_names

    def get_node_name(self):
        return self.node_name

# This function is used to initialize the state space 
def initialize_graph():

    graph = { 'A': ['B','C', 'E'],
              'B': ['A', 'D', 'E'],
              'C': ['A', 'D'],
              'D': ['B', 'C'],
              'E': ['A', 'B'] }

    costs = { ('A','E'): 5,
              ('A', 'B'): 3,
              ('A', 'C'): 3,
              ('B','E'): 1,
              ('B', 'D'): 2,
              ('C', 'D'): 1 }
    return graph , costs

#this function is called to initialise the heuristic according to the board size
def heuristic(node1, node2, graph_size):

    if(node1 == node2):
        return 0

    node1 = node1.get_node_name()
    node2 = node2.get_node_name()
    start = node1[0] + node1[1]
    goal = node2[0] + node2[1]

    diagonal = False
    for x in range(0,graph_size):
        if(((x + node1[0] == node2[0]) |
               (x - node1[0] == node2[0])) &
               ((x + node1[1] == node2[1]) |
               (x - node1[1] == node2[1]))):
            diagonal = True
            break

    two_distance_square = False
    if(((2 + node1[0] == node2[0]) | (2 - node1[0] == node2[0]))& ((2 + node1[1] == node2[1]) | (2 - node1[1] == node2[1]))):
        two_distance_square = True

    color = (start & 0x1 ) ==  (goal & 0x1 )

    manhattan = abs(node1[0] - node2[0] ) + abs(node1[1] - node2[1] )

    outside_four_box = False
    if (((node1[0] + 4 < node1[0] | node1[0] - 4 > node1[0]) |
                (node1[1] + 4 < node1[1] | node1[1] - 4 > node1[1]))):
        outside_four_box = True

    min_distance = 1

    if((not color )& (not two_distance_square)):
        min_distance = max(3,min_distance)
    if (color): 
        min_distance = max(2, min_distance)

    if (diagonal & (manhattan % 4 == 0)):
        min_distance = max(4, min_distance)
    if(color & outside_four_box) :
        min_distance = max(4,min_distance)


    return min_distance



class Stack():

    def __init__(self):
        self.ordered_stack = [] 

    def add_node(self, node, cost):
        self.ordered_stack.append((node,cost))
        self.ordered_stack =  sorted(self.ordered_stack, key=itemgetter(1))


    def pop_node(self):
        return self.ordered_stack.pop(0) 




def a_star(x1,y1,x2,y2,size):

    graph_size = size
    graph = build_graph(graph_size)

    nodes = {}

    for key, value in graph.items():
        nodes[key] = Node(key, value)

    stack = Stack()

    start = nodes[(x1,y1)]
    goal = nodes[(x2,y2)]

    stack.add_node(start, 0)
    start.set_cost(0)

    count=0

    t = time.time()
    while bool(stack):
        stack_item = stack.pop_node()
        count+=1
        #currenct_h_cost = stack_item[1]
        current_node = stack_item[0]
        current_cost = current_node.get_cost()

        print("Parent Node = %s current cost = %s heuristic = %s" %(current_node.get_node_name(), current_cost, heuristic(current_node, goal, graph_size)))
        if current_node == goal:
            print("found goal")
            break

        for child_name in current_node.get_children():

            new_cost = current_cost + 1 #costs[sorted_nodes[0],sorted_nodes[1]]
            child = nodes[child_name]
            if(child.get_cost() > new_cost ):

                print("New Path from %s to %s with total cost %s" %(current_node.get_node_name(), child_name, new_cost))
                child.set_cost(new_cost )
                child.set_parent(current_node)
                stack.add_node(child, new_cost + heuristic(child, goal, graph_size))
    exec_time=time.time() - t
    print 'Time to generate the route (seconds): ', exec_time
    print("Path :")
    parent = goal.get_parent()
    print(goal.get_node_name())
    while(parent is not None):
        
        print(parent.get_node_name())
        parent = nodes[parent.get_node_name()].get_parent()

    print("cost = %s" %(goal.get_cost()))
    return count, goal.get_cost(), exec_time


def add_edge(graph, vertex_a, vertex_b):
    graph[vertex_a].add(vertex_b)
    graph[vertex_b].add(vertex_a)


def build_graph(board_size):
    graph = defaultdict(set)
    for row in range(board_size):
        for col in range(board_size):
            for to_row, to_col in legal_moves_from(row, col, board_size):
                add_edge(graph, (row, col), (to_row, to_col))
    return graph




## this is what gives the legal moves for the knights 
def legal_moves_from(row, col, board_size):
    MOVE_OFFSETS = (
        (-1, -2), (1, -2),
        (-2, -1), (2, -1),
        (-2, 1), (2, 1),
        (-1, 2), (1, 2),
    )
    for row_offset, col_offset in MOVE_OFFSETS:
        move_row, move_col = row + row_offset, col + col_offset
        if 0 <= move_row < board_size and 0 <= move_col < board_size:
            yield move_row, move_col


if __name__=="__main__":
    counts=[]
    costs=[]
    times=[]
    
    graph_size=8
    for i in range(100):
        x,y,z=a_star(np.random.randint(0,8),np.random.randint(0,8),np.random.randint(0,8),np.random.randint(0,8),graph_size)
        counts.append(x)
        costs.append(y)
        times.append(z)
    #print len(counts)
    #print len(costs)
    
    
    fig=plt.figure()
    for i in range(100):
        plt.scatter(costs[i],counts[i])
    #plt.show()
    plt.xlabel('Solution length', fontsize=18)
    plt.ylabel('Number of nodes expanded', fontsize=16)
    fig.savefig('Nodes vs Solution Length.jpg')
    
    
    fig2=plt.figure()
    for i in range(100):
        plt.scatter(costs[i],times[i])
    #plt.show()
    plt.xlabel('Solution length', fontsize=18)
    plt.ylabel('Time to completion', fontsize=16)
    fig2.savefig('Time vs Solution Length.jpg')




