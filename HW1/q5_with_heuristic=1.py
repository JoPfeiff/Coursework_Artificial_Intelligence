

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


    #def set_shortest_distance(self,distance, path):

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

def heuristic(node1, node2):
    return 1



class Stack():

    def __init__(self):
        self.ordered_stack = [] #collections.OrderedDict(reversed = False)

    def add_node(self, node, cost):
        #self.ordered_stack[node] = cost
        self.ordered_stack.append((node,cost))
        self.ordered_stack =  sorted(self.ordered_stack, key=itemgetter(1))
        #print(self.ordered_stack)

    def pop_node(self):
        return self.ordered_stack.pop(0) #popped_node = self.ordered_stack.items()[0]




def a_star(x1,y1,x2,y2):

    #graph, costs = initialize_graph()

    graph = build_graph(8)

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
        currenct_h_cost = stack_item[1]
        count+=1
        current_node = stack_item[0]
        current_cost = current_node.get_cost()

        print("Parent Node = %s current cost = %s heuristic = %s" %(current_node.get_node_name(), current_cost, currenct_h_cost))
        if current_node == goal:
            print("found goal")
            break

        for child_name in current_node.get_children():

            sorted_nodes = sorted([current_node.get_node_name(), child_name])
            new_cost = current_cost + 1 #costs[sorted_nodes[0],sorted_nodes[1]]
            child = nodes[child_name]
            if(child.get_cost() > new_cost ):
                
                print("New Path from %s to %s with total cost %s" %(current_node.get_node_name(), child_name, new_cost))
                child.set_cost(new_cost )
                child.set_parent(current_node)
                stack.add_node(child, new_cost + heuristic(child, goal))
    exec_time=time.time() - t
    print 'Time to generate the route (seconds): ', exec_time
    print("Path :")
    parent = goal.get_parent()
    print(goal.get_node_name())
    while(parent is not None):
        
        print(parent.get_node_name())
        parent = nodes[parent.get_node_name()].get_parent()

    print("cost = %s" %(goal.get_cost()))
    print count
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

counts=[]
costs=[]
times=[]
for i in range(100):
    x,y,z=a_star(np.random.randint(0,8),np.random.randint(0,8),np.random.randint(0,8),np.random.randint(0,8))
    counts.append(x)
    costs.append(y)
    times.append(z)
#print len(counts)
#print len(costs)

for i in range(100):
    plt.scatter(costs[i],counts[i])
plt.show()
plt.savefig("scatterplot.pdf")

for i in range(100):
    plt.scatter(costs[i],times[i])
plt.show()
    

