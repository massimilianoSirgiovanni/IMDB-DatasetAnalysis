import networkx as nx
from yearsFunctions import createSetUpToYear
import time
from math import ceil

def diameterUpToYear(x, graph):

    start_time = time.time()
    setYear = createSetUpToYear(x)
    end_time = time.time()
    print(f"EXECUTION TIME: {end_time - start_time}")
    start_time = time.time()
    maxGrade = nodeGradeMax(graph, setYear)
    end_time = time.time()
    print(f"EXECUTION TIME: {end_time - start_time}")
    start_time = time.time()
    startNode = doubleSweep(graph, maxGrade, setYear)
    end_time = time.time()
    print(f"EXECUTION TIME: {end_time - start_time}")
    diam = diameter(graph, startNode, setYear)
    return diam


def nodeGradeMax(graph, set):
    maxN = -1  # Variable to store the id of the current
    sumMax = 0
    giant = max(nx.connected_components(graph.subgraph(set)), key=len)
    for i in giant:
        degreeNode = graph.degree(i)
        if degreeNode > sumMax:
            sumMax = degreeNode
            maxN = i
    if maxN == -1:
        print("ERROR: NO NODE FOUND IN THE GRAPH")
        return -1
    else:
        return maxN


def doubleSweep(graph, node, set):
    ecc = bfs(graph, node, set)
    ecc2 = bfs(graph, ecc[1][ecc[0]][0], set)
    print(ecc2[0])
    R = ceil(ecc2[0]/2)
    print(ecc2[2])
    print(ecc2[2][R])
    return ecc2[2][R]


def bfs(graph, startNode, setNode):
    eccPath = {startNode: [startNode]}
    distancesToNodes = {}

    nodeDistance = {startNode: 0}

    nodeToVisit = [startNode]
    index = 0
    max = 0

    while index < len(nodeToVisit):
        currentVert = nodeToVisit[index]
        neighbors = list(graph.neighbors(currentVert))

        for nbr in neighbors:
            if nbr in setNode:
                if nbr not in nodeDistance:
                    eccPath[nbr] = eccPath[currentVert].copy()
                    eccPath[nbr].append(nbr)
                    nodeToVisit.append(nbr)
                    nodeDistance[nbr] = nodeDistance[currentVert] + 1
                    if nodeDistance[nbr] not in distancesToNodes:
                        distancesToNodes[nodeDistance[nbr]] = [nbr]
                    else:
                        distancesToNodes[nodeDistance[nbr]].append(nbr)

                    if nodeDistance[nbr] > max:
                        max = nodeDistance[nbr]
        index = index + 1
    '''print(eccPath)
    print(len(eccPath)-1)'''
    for i in eccPath:
        if len(eccPath[i]) - 1 == max:
            return (max, distancesToNodes, eccPath[i])
    return 0




# Calcolo dell'eccentricità
def eccentricity(graph, startNode, set):
    max = bfs(graph, startNode, set)

    return max


#def Bi(graph, node, lb, level):
def Bi(graph, nodeList, lb, set):
    for i in nodeList:
        temp = eccentricity(graph, i, set)
        if temp[0] > lb:
            return temp[0]

    return lb
    '''for j in graph.nodes:
        distance = len(nx.shortest_path(graph, node, j))-1
        if distance == level:
            ecc = nx.eccentricity(graph, j)
            if ecc > lb:
                return ecc
    return lb'''



'''def diameter(graph, startNode):
    ecc = nx.eccentricity(graph, startNode)
    i = ecc
    lb = i
    ub = 2 * lb

    while ub > lb:

        bi = Bi(graph, startNode, lb, i)

        if bi > 2 * (i - 1):
            return bi
        else:
            lb = bi
            ub = 2 * (i - 1)
        i = i - 1

    return lb'''

def diameter(graph, startNode, setNode):
    start_time = time.time()
    bfsTuple = eccentricity(graph, startNode, setNode)
    end_time = time.time()
    print(f"Compute bfsTuple TIME: {end_time - start_time}")
    i = bfsTuple[0]
    lb = i
    ub = 2 * lb

    while ub > lb:
        start_time = time.time()
        bi = Bi(graph, bfsTuple[1][i], lb, setNode)
        end_time = time.time()
        print(f"Bi() at {i} level TIME: {end_time - start_time}: with {bi}")


        if bi > 2 * (i - 1):
            return bi
        else:
            lb = bi
            ub = 2 * (i - 1)
        i = i - 1

    return lb


