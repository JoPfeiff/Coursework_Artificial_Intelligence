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




def prim(G,start):
    pq = PriorityQueue()
    for v in G:
        v.setDistance(sys.maxsize)
        v.setPred(None)
    start.setDistance(0)
    pq.buildHeap([(v.getDistance(),v) for v in G])
    while not pq.isEmpty():
        currentVert = pq.delMin()
        for nextVert in currentVert.getConnections():
          newCost = currentVert.getWeight(nextVert)
          if nextVert in pq and newCost<nextVert.getDistance():
              nextVert.setPred(currentVert)
              nextVert.setDistance(newCost)
              pq.decreaseKey(nextVert,newCost)