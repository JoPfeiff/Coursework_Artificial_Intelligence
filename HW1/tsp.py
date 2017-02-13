import numpy as np
from pythonds.graphs import PriorityQueue, Graph, Vertex

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


simple_generator(5)



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

def build_graph(points):
    #points = simple_generator(graph_size)

    graph = {}

    for point_p in points:

        distance_dict = {}

        for point_c in points:

            if point_c != point_p:

                distance_dict[point_c] = distance(point_c,point_p)

        graph[Node(point_p,distance_dict)] = 0
    return graph


def build_TSP_Graph(graph_size):
    points = simple_generator(graph_size)

    start_name = points[0]
    all_nodes = {}
    for point_p in points:

        distance_dict = {}

        for point_c in points:

            if point_c != point_p:

                distance_dict[point_c] = distance(point_c,point_p)

        all_nodes[point_p] = Node(point_p,distance_dict)

    start_node = all_nodes[start_name]

    #for key, value in  graph.iteritems():

    graph = []
    #graph[0] = start_node
    for i in range(len(points)):
        if points[i] != start_name:
            graph.append(points[i])




def a_star(x1, y1, x2, y2):
    # graph, costs = initialize_graph()
    graph_size = 8
    graph = build_graph(graph_size)

    nodes = {}

    for key, value in graph.items():
        nodes[key] = Node(key, value)

    stack = Stack()

    start = nodes[(x1, y1)]
    goal = nodes[(x2, y2)]

    stack.add_node(start, 0)
    start.set_cost(0)

    count = 0

    t = time.time()
    while bool(stack):
        stack_item = stack.pop_node()
        currenct_h_cost = stack_item[1]
        current_node = stack_item[0]
        current_cost = current_node.get_cost()

        print("Parent Node = %s current cost = %s heuristic = %s" % (
        current_node.get_node_name(), current_cost, heuristic(current_node, goal, graph_size)))
        if current_node == goal:
            print("found goal")
            break

        for child_name in current_node.get_children():

            sorted_nodes = sorted([current_node.get_node_name(), child_name])
            new_cost = current_cost + 1  # costs[sorted_nodes[0],sorted_nodes[1]]
            child = nodes[child_name]
            if (child.get_cost() > new_cost):
                count += 1
                print(
                "New Path from %s to %s with total cost %s" % (current_node.get_node_name(), child_name, new_cost))
                child.set_cost(new_cost)
                child.set_parent(current_node)
                stack.add_node(child, new_cost + heuristic(child, goal, graph_size))
    exec_time = time.time() - t
    print 'Time to generate the route (seconds): ', exec_time
    print("Path :")
    parent = goal.get_parent()
    print(goal.get_node_name())
    while (parent is not None):
        print(parent.get_node_name())
        parent = nodes[parent.get_node_name()].get_parent()

    print("cost = %s" % (goal.get_cost()))
    print count
    return count, goal.get_cost(), exec_time


def popmin(pqueue):
    # A (ascending or min) priority queue keeps element with
    # lowest priority on top. So pop function pops out the element with
    # lowest value. It can be implemented as sorted or unsorted array
    # (dictionary in this case) or as a tree (lowest priority element is
    # root of tree)
    lowest = 1000
    keylowest = None
    for key in pqueue:
        if pqueue[key] < lowest:
            lowest = pqueue[key]
            keylowest = key
    del pqueue[keylowest]
    return keylowest


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
    return pred


def distance(node1, node2):
    return (abs(node1[0] - node2[0]) **2 +   abs(node1[1] - node2[1]) **2) ** 0.5


graph = {0: {1: 6, 2: 8},
         1: {4: 11},
         2: {3: 9},
         3: {},
         4: {5: 3},
         5: {2: 7, 3: 4}}

pred = prim(graph, 0)
for v in pred: print "%s: %s" % (v, pred[v])



