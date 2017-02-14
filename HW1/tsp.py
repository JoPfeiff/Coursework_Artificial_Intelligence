import numpy as np
from pythonds.graphs import PriorityQueue, Graph, Vertex
import itertools
import collections
from operator import itemgetter
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import time
import copy

def simple_generator(nr_samples):
    points = [None] * nr_samples
    i = 0
    while i <  nr_samples:
        tup = (np.random.random(1)[0],np.random.random(1)[0])
        if tup in points:
            i=i
        else:
            points[i] = tup
            i += 1
    return points


def distance(node1, node2):
    return (abs(node1[0] - node2[0]) **2 +   abs(node1[1] - node2[1]) **2) ** 0.5

def prim(graph, root):
    pred = {}  # pair {vertex: predecesor in MST}
    key = {}  # keep track of minimum weight for each vertex
    pqueue = {}  # priority queue implemented as dictionary

    for v in graph:
        pred[v] = -1
        key[v] = 1000
        if v == root:
            key[root] = 0
        pqueue[v] = key[v]
    #for v in graph:


    while pqueue:
        u = popmin(pqueue)
        for v in graph[u]:  # all neighbors of v
            if v in pqueue and graph[u][v] < key[v]:
                pred[v] = u
                key[v] = graph[u][v]
                pqueue[v] = graph[u][v]
    cost = 0
    for key, value in pred.iteritems():
        if value != -1:
            cost += distance(key,value)

    return cost


def popmin(pqueue):
    # A (ascending or min) priority queue keeps element with
    # lowest priority on top. So pop function pops out the element with
    # lowest value. It can be implemented as sorted or unsorted array
    # (dictionary in this case) or as a tree (lowest priority element is
    # root of tree)
    lowest = 999999999999999
    keylowest = None
    for key in pqueue:
        if pqueue[key] < lowest:
            lowest = pqueue[key]
            keylowest = key
    del pqueue[keylowest]
    return keylowest



class Node():

    parent_node = None
    cost = 999999999999999

    def __init__(self, node_name, child_node_names, missing):
        self.node_name = node_name
        #self.parent_node_name = parent_node_name
        #self.child_node_names = {}
        self.child_node_names = child_node_names
        self.missing = missing


    #def set_shortest_distance(self,distance, path):

    def get_missing(self):
        return self.missing

    def set_parent(self, parent_node):
        self.parent_node = parent_node

    def set_cost(self, cost):
        self.cost = cost

    def get_parent(self):
        return self.parent_node

    def get_cost(self):
        return  self.cost

    def add_child(self, child):
        self.child_node_names.append(child)
        return self.child_node_names

    def get_children(self):
        return self.child_node_names

    def get_node_name(self):
        return self.node_name

    def get_last_elem(self):
        return self.node_name[-1]



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

def build_MST_graph(points):
    #points = simple_generator(graph_size)

    graph = {}

    for point_p in points:

        distance_dict = {}

        for point_c in points:

            if point_c != point_p:

                try:
                    bool(graph[point_p])
                except:
                    graph[point_p] ={}
                graph[point_p][point_c] = distance(point_c,point_p)

        #graph[Node(point_p,distance_dict)] = 0
    return graph



def build_TSP_Graph(points):

    graph = {}


    all_nodes = {}

    for subset in itertools.permutations(points, len(points)):

        tup_set = []

        for i in range(0,len(subset)):
            tup_set.append(subset[i])
            missing = []
            for s in subset:
                if s not in tup_set:
                    missing.append(s)
            if not all_nodes.has_key(str(tup_set)) :
                current_missing = copy.copy(missing)
                current_tup_set = copy.copy(tup_set)
                all_nodes[str(tup_set)] = Node(current_tup_set,[], current_missing)


        tup_set = []
        child_tup_set = []
        for i in range(0,len(subset)):
            tup_set.append(subset[i])
            if i == 0:
                child_tup_set.append(subset[i])



            if i < len(subset) - 1:
                child_tup_set.append(subset[i+1])
                cost = distance(subset[i], subset[i+1])

                try:
                    bool(graph[all_nodes[str(tup_set)]])

                except:
                    graph[all_nodes[str(tup_set)]] = {}

                current_children = copy.copy(child_tup_set)

                all_nodes[str(tup_set)].add_child(current_children)
                child_node = all_nodes[str(child_tup_set)]
                graph[all_nodes[str(tup_set)]][child_node] =  cost
            else:
                graph[str(tup_set)] = None #(tup_set, None, 0)

    print("TSP Graph was set")
    return graph, all_nodes

#points = simple_generator(5)

#graph =  build_TSP_Graph(points)
#print graph

def heuristic(conn_node, start, missing_nodes):

    start = start.get_last_elem()
    closest_connection = 999999999999999999999
    closest_start = 999999999999999999999


    for node in missing_nodes:
        to_start = distance(start,node)
        to_conn = distance(node,conn_node)
        closest_connection = max(to_conn,closest_connection)
        closest_start = max(closest_start,to_start)


    if(missing_nodes == []):
        return closest_connection + closest_start

    graph = build_MST_graph(missing_nodes)

    mst_cost = prim(graph, missing_nodes[0])

    return closest_connection + closest_start + mst_cost




def a_star(points):

    allStart = time.time()
    graph, all_nodes = build_TSP_Graph(points)


    stack = Stack()

    start = all_nodes[str([points[0]])]#nodes[(x1, y1)]


    stack.add_node(start, 0)
    start.set_cost(0)

    count = 0

    t = time.time()
    current_node = None
    while bool(stack):
        stack_item = stack.pop_node()
        currenct_h_cost = stack_item[1]
        current_node = stack_item[0]
        current_cost = current_node.get_cost()

        #print("Parent Node = %s current cost = %s heuristic = %s" % (
        #current_node.get_node_name(), current_cost, heuristic(current_node, goal, graph_size)))
        if current_node.get_children() == []:
            print("found goal")
            break

        for child_name in current_node.get_children():

            sorted_nodes = sorted([current_node.get_node_name(), child_name])
            #test = graph[all_nodes[str(current_node[0])]]
            child_node = all_nodes[str(child_name)]
            test = graph[current_node][child_node]
            new_cost = current_cost + graph[current_node][child_node]  # costs[sorted_nodes[0],sorted_nodes[1]]
            child = all_nodes[str(child_name)]
            if (child.get_cost() > new_cost):
                count += 1
                #print(
                #"New Path from %s to %s with total cost %s" % (current_node.get_node_name(), child_name, new_cost))
                child.set_cost(new_cost)
                child.set_parent(current_node)
                stack.add_node(child, new_cost + heuristic(child.get_last_elem(), start, child.get_missing()))
    exec_time = time.time() - t
    endtime = time.time() - allStart
    print "Time for everything: %s" %(endtime)
    print 'Time to generate the route (seconds): ', exec_time
    print("Path :")
    parent = current_node.get_parent()
    print(current_node.get_node_name())
    while (parent is not None):
        print(parent.get_node_name())
        parent = parent.get_parent()

    print("cost = %s" % (current_node.get_cost()))
    print count
    return count, current_node.get_cost(), exec_time



def load_points(file):
    with open(file) as f:
        content = f.readlines()
    points = []
    for line in content:

        if line[0].isdigit():
            split = line.split(" ")
            tup = (float(split[1]), float(split[2]))
            points.append(tup)
    return points

file = "Data/dj38.tsp.txt"

points = load_points(file)

graph_size = 8
points = simple_generator(graph_size)



a_star(points)




#points = simple_generator(5)

#graph = build_MST_graph(points)
#print graph

#cost = prim(graph, points[0])
#print "cost: %s" %(cost)
#for v in pred: print "%s: %s" % (v, pred[v])



